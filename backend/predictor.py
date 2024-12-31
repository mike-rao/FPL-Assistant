import joblib
import pandas as pd
from database import get_players_from_db

model = joblib.load('fpl_model.pkl')
player_dataset = get_players_from_db

def predict_player_points(player_data):
    """
    Predict FPL points for a given player using the trained model.
    player_data: dict with keys ['form', 'pts_per_match', 'total_pts', 'ict_index', 'tsb_percent', 'fdr']
    """
    features = pd.DataFrame([{
        'form': player_data['form'],
        'pts_per_match': player_data['pts_per_match'],
        'total_pts': player_data['total_pts'],
        'ict_index': player_data['ict_index'],
        'tsb_percent': player_data['tsb_percent'],
        'fdr': player_data['fdr']
    }])
    predicted_points = model.predict(features)
    return predicted_points[0]

def suggest_transfers(current_team, free_transfers, transfer_budget, player_dataset):
    """
    Suggest transfers to maximize points within budget.
    """
    def find_replacements(player, budget):
        position_mapping = {
            1: "Goalkeeper",
            2: "Defender",
            3: "Midfielder",
            4: "Forward"
        }
        player_position = position_mapping.get(player["position"]) 
        filter1 = list(filter(lambda p: p["position"] == player_position, player_dataset))
        filter2 = list(filter(lambda p: p["price"] <= player["price"] + budget, filter1))
        filter3 = list(filter(lambda p: p["name"] not in ([n["name"] for n in current_team]), filter2))
        eligible_players = list(filter(lambda p: p["name"] not in ([n["name"] for n in transfered_out]), filter3))
        return sorted(eligible_players, key=lambda p: p["predicted_points"])

    transfers = []
    transfered_out = []
    remaining_budget = transfer_budget
    for _ in range(free_transfers):
        best_transfer = None
        best_gain = -float("inf")
        for player in current_team:
            replacements = find_replacements(player, remaining_budget)
            if len(replacements) > 0:
                replacement = replacements[0]
                player["predicted_points"] = list(filter(lambda p: p["name"] == player["name"], player_dataset))[0]["predicted_points"]
                gain = replacement["predicted_points"] - player["predicted_points"]

                if gain > best_gain:
                    best_gain = gain
                    best_transfer = {
                        "transfer_out": player,
                        "transfer_in": replacement
                    }

        if best_transfer:
            transfers.append(best_transfer)
            remaining_budget -= best_transfer["transfer_in"]["price"] - best_transfer["transfer_out"]["price"]
            current_team.remove(best_transfer["transfer_out"])
            current_team.append(best_transfer["transfer_in"])
            transfered_out.append(best_transfer["transfer_out"])
            print(best_transfer["transfer_in"]["name"], "net gain:", best_transfer["transfer_in"]["predicted_points"] - best_transfer["transfer_out"]["predicted_points"])

    return transfers


# Testing
# player = {
#     'form': 4.4,
#     'pts_per_match': 5.6,
#     'total_pts': 90,
#     'ict_index': 91.6,
#     'tsb_percent': 24.1,
#     'fdr': 3
# }
# predicted_points = predict_player_points(player)
# print(f"Predicted Points for Next Week: {predicted_points}")