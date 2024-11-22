from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import scrape_fpl_data
from data_cleaner import clean_and_preprocess_data

app = Flask(__name__)
CORS(app)

@app.route('/get_player_data', methods=['GET'])
def get_player_data():
    player_data = [
        {"id": 1, "first_name": "Erling", "second_name": "Haaland", "team": "Manchester City", "element_type": "FWD", "now_cost": 12.2, "total_points": 100},
        {"id": 2, "first_name": "Mohamed", "second_name": "Salah", "team": "Liverpool", "element_type": "MID", "now_cost": 12.8, "total_points": 90},
        {"id": 3, "first_name": "Harry", "second_name": "Kane", "team": "Tottenham", "element_type": "FWD", "now_cost": 10.9, "total_points": 85},
    ]
    return jsonify(player_data)  # Return as JSON

if __name__ == '__main__':
    app.run(debug=True)