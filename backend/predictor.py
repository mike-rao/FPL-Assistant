from database import get_players_from_db

player_dataset = get_players_from_db()

def predict_player_points(player_data):
    """
    Predict FPL points for a given player using the trained model.
    player_data: dict with keys ['position', 'form', 'pts_per_match', 'total_pts', 'total_bonus', 'ict_index', 'tsb_percent', 'fdr']
    """
    import joblib
    import pandas as pd
    
    model = joblib.load('fpl_model.pkl')
    scaler = joblib.load('scaler.pkl')
    
    features = pd.DataFrame([{
        'position': player_data['position'],
        'form': player_data['form'],
        'pts_per_match': player_data['pts_per_match'],
        'total_pts': player_data['total_pts'],
        'total_bonus': player_data['total_bonus'],
        'ict_index': player_data['ict_index'],
        'tsb_percent': player_data['tsb_percent'],
        'fdr': player_data['fdr']
    }])
    
    scaled_features = scaler.transform(features)
    
    predicted_points = model.predict(scaled_features)
    return predicted_points[0]

def suggest_transfers(current_team, free_transfers, transfer_budget, player_dataset):
    """
    Suggest transfers to maximize predicted points gain within budget constraints.
    """
    from collections import defaultdict
        
    players_by_position = defaultdict(list)
    for player in player_dataset:
        players_by_position[player["position"]].append(player)
        
    for position in players_by_position:
        players_by_position[position].sort(key=lambda p: p["predicted_points"], reverse=True)
    
    def find_best_replacement(player, remaining_budget):
        eligible_players = players_by_position.get(player["position"], [])
        for replacement in eligible_players:
            if replacement["price"] <= player["price"] + remaining_budget and replacement["name"] not in current_names:
                print(f"Selected replacement: {replacement['name']} for {player['name']}")
                return replacement
        print(f"No replacements found for player: {player['name']}")
        return None

    transfers = []
    current_names = {player["name"] for player in current_team}
    remaining_budget = transfer_budget

    for _ in range(free_transfers):
        best_transfer = None
        best_gain = -float("inf")
        for player in current_team:
            replacement = find_best_replacement(player, remaining_budget)
            player["predicted_points"] = list(filter(lambda p: p["name"] == player["name"], player_dataset))[0]["predicted_points"]
            if replacement:
                gain = replacement["predicted_points"] - player["predicted_points"]
                if gain > best_gain:
                    best_gain = gain
                    best_transfer = {
                        "transfer_out": player,
                        "transfer_in": replacement
                    }
        if not best_transfer:
            break
        
        transfers.append(best_transfer)
        remaining_budget -= best_transfer["transfer_in"]["price"] - best_transfer["transfer_out"]["price"]
        current_team.remove(best_transfer["transfer_out"])
        current_team.append(best_transfer["transfer_in"])
        current_names.add(best_transfer["transfer_in"]["name"])

        print(f"Transfer Out: {best_transfer['transfer_out']['name']} ({best_transfer['transfer_out']['predicted_points']} pts) -> ")
        print(f"Transfer In: {best_transfer['transfer_in']['name']} ({best_transfer['transfer_in']['predicted_points']} pts) | ")
        print(f"Net Gain: {best_gain:.2f}")

    return transfers