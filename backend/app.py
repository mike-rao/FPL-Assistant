from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import scrape_stats
from database import save_to_database, get_players_from_db
from predictor import predict_player_points, suggest_transfers

app = Flask(__name__)
CORS(app)
    
@app.route('/scrape-and-save', methods=['POST'])
def scrape_and_save():
    try:
        players = scrape_stats()
        save_to_database(players)
        return jsonify({"message": "Data scraped and saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to scrape and save data: {e}"}), 500

@app.route('/players', methods=['GET'])
def fetch_players():
    try:
        players = get_players_from_db()
        return jsonify(players), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch players: {e}"}), 500
    
@app.route('/predict-pts', methods=['POST'])
def predict_player_pts():
    try:
        players = request.json.get('players', [])
        if not players:
            return jsonify({"error": "No players provided."}), 400
        
        for player in players:
            player['xpts'] = predict_player_points(player)
        
        players.sort(key=lambda p: p['xpts'], reverse=True)
        return jsonify(players), 200
    except Exception as e:
        return jsonify({"error": f"Failed to predict player pts: {e}"}), 500
    
@app.route('/suggest-transfers', methods=['POST'])
def suggest_player_transfers():
    try:
        data = request.json
        current_team = data.get("current_team", [])
        free_transfers = data.get("free_transfers", 0)
        transfer_budget = data.get("transfer_budget", 0.0)
        
        player_dataset = get_players_from_db()
        position_mapping = {"Goalkeeper": 1,"Defender": 2,"Midfielder": 3,"Forward": 4}
        for player in player_dataset:
            player["position"] = position_mapping.get(player["position"])
            player["predicted_points"] = predict_player_points(player)
        
        transfer_suggestions = suggest_transfers(current_team, free_transfers, transfer_budget, player_dataset)
        sorted_transfers = sorted(
            transfer_suggestions,
            key=lambda x: x["transfer_in"]["predicted_points"] - x["transfer_out"]["predicted_points"],
            reverse=True
        )
        return jsonify(sorted_transfers), 200
    except Exception as e:
        return jsonify({"error": f"Failed to suggest transfers: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)