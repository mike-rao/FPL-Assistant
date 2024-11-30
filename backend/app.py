from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import scrape_fpl_data
from data_cleaner import clean_and_preprocess_data

app = Flask(__name__)
CORS(app)

@app.route('/get_player_data', methods=['GET'])
def get_player_data():
    player_data = [
        {"id": 1, "first_name": "Erling", "last_name": "Haaland", "team": "Manchester City", "position": "FWD", "price": 12.2, "form": 9.5, "pts_per_match": 10.0, "total_pts": 100, "total_bonus": 20, "ict_index": 120.0, "tsb%": 85.5},
        {"id": 2, "first_name": "Mohamed", "last_name": "Salah", "team": "Liverpool", "position": "MID", "price": 12.8, "form": 8.0, "pts_per_match": 9.0, "total_pts": 90, "total_bonus": 18, "ict_index": 115.0, "tsb%": 70.2},
        {"id": 3, "first_name": "Harry", "last_name": "Kane", "team": "Tottenham", "position": "FWD", "price": 10.9, "form": 7.8, "pts_per_match": 8.5, "total_pts": 85, "total_bonus": 16, "ict_index": 110.0, "tsb%": 65.8},
        {"id": 4, "first_name": "Kevin", "last_name": "De Bruyne", "team": "Manchester City", "position": "MID", "price": 11.5, "form": 7.5, "pts_per_match": 8.0, "total_pts": 80, "total_bonus": 15, "ict_index": 105.0, "tsb%": 68.1},
        {"id": 5, "first_name": "Marcus", "last_name": "Rashford", "team": "Manchester United", "position": "MID", "price": 9.5, "form": 6.5, "pts_per_match": 7.5, "total_pts": 75, "total_bonus": 14, "ict_index": 95.0, "tsb%": 55.0},
        {"id": 6, "first_name": "Trent", "last_name": "Alexander-Arnold", "team": "Liverpool", "position": "DEF", "price": 7.5, "form": 6.0, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 12, "ict_index": 90.0, "tsb%": 60.3},
        {"id": 7, "first_name": "Nick", "last_name": "Pope", "team": "Newcastle", "position": "GKP", "price": 5.5, "form": 5.5, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 10, "ict_index": 85.0, "tsb%": 50.0},
        {"id": 8, "first_name": "Bukayo", "last_name": "Saka", "team": "Arsenal", "position": "MID", "price": 8.2, "form": 6.0, "pts_per_match": 7.2, "total_pts": 72, "total_bonus": 13, "ict_index": 92.0, "tsb%": 58.7},
        {"id": 9, "first_name": "Gabriel", "last_name": "Jesus", "team": "Arsenal", "position": "FWD", "price": 8.0, "form": 6.2, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 11, "ict_index": 88.0, "tsb%": 54.9},
        {"id": 10, "first_name": "James", "last_name": "Ward-Prowse", "team": "West Ham", "position": "MID", "price": 6.5, "form": 5.5, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 49.2},
        {"id": 11, "first_name": "Son", "last_name": "Heung-Min", "team": "Tottenham", "position": "MID", "price": 9.8, "form": 7.0, "pts_per_match": 8.2, "total_pts": 82, "total_bonus": 15, "ict_index": 102.0, "tsb%": 63.5},
        {"id": 12, "first_name": "Alexander", "last_name": "Isak", "team": "Newcastle", "position": "FWD", "price": 7.8, "form": 6.0, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 10, "ict_index": 82.0, "tsb%": 48.0},
        {"id": 13, "first_name": "Kieran", "last_name": "Trippier", "team": "Newcastle", "position": "DEF", "price": 6.8, "form": 7.5, "pts_per_match": 7.8, "total_pts": 78, "total_bonus": 13, "ict_index": 95.0, "tsb%": 57.3},
        {"id": 14, "first_name": "Alisson", "last_name": "Becker", "team": "Liverpool", "position": "GKP", "price": 5.4, "form": 5.5, "pts_per_match": 6.4, "total_pts": 64, "total_bonus": 8, "ict_index": 83.0, "tsb%": 46.9},
        {"id": 15, "first_name": "Martin", "last_name": "Ødegaard", "team": "Arsenal", "position": "MID", "price": 7.5, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 12, "ict_index": 90.0, "tsb%": 51.8},
        {"id": 16, "first_name": "Ivan", "last_name": "Toney", "team": "Brentford", "position": "FWD", "price": 7.0, "form": 6.0, "pts_per_match": 6.6, "total_pts": 66, "total_bonus": 11, "ict_index": 88.0, "tsb%": 47.5},
        {"id": 17, "first_name": "Virgil", "last_name": "van Dijk", "team": "Liverpool", "position": "DEF", "price": 6.3, "form": 5.0, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 9, "ict_index": 80.0, "tsb%": 43.1},
        {"id": 18, "first_name": "Aaron", "last_name": "Ramsdale", "team": "Arsenal", "position": "GKP", "price": 5.2, "form": 5.0, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 9, "ict_index": 80.0, "tsb%": 40.2},
        {"id": 19, "first_name": "Phil", "last_name": "Foden", "team": "Manchester City", "position": "MID", "price": 7.2, "form": 6.5, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 12, "ict_index": 88.0, "tsb%": 50.4},
        {"id": 20, "first_name": "Raheem", "last_name": "Sterling", "team": "Chelsea", "position": "MID", "price": 7.5, "form": 5.8, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 10, "ict_index": 82.0, "tsb%": 45.8},
        {"id": 21, "first_name": "Ederson", "last_name": "Moraes", "team": "Manchester City", "position": "GKP", "price": 5.8, "form": 6.0, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 11, "ict_index": 87.0, "tsb%": 48.2},
        {"id": 22, "first_name": "João", "last_name": "Cancelo", "team": "Barcelona", "position": "DEF", "price": 7.0, "form": 6.5, "pts_per_match": 7.2, "total_pts": 72, "total_bonus": 13, "ict_index": 92.0, "tsb%": 52.5}, 
        {"id": 23, "first_name": "Reece", "last_name": "James", "team": "Chelsea", "position": "DEF", "price": 6.0, "form": 5.5, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 10, "ict_index": 80.0, "tsb%": 45.0},
        {"id": 24, "first_name": "Andrew", "last_name": "Robertson", "team": "Liverpool", "position": "DEF", "price": 6.8, "form": 6.0, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 12, "ict_index": 88.0, "tsb%": 48.7},
        {"id": 25, "first_name": "Bruno", "last_name": "Fernandes", "team": "Manchester United", "position": "MID", "price": 8.5, "form": 7.0, "pts_per_match": 7.8, "total_pts": 78, "total_bonus": 14, "ict_index": 98.0, "tsb%": 55.3},
        {"id": 26, "first_name": "João", "last_name": "Felix", "team": "Chelsea", "position": "MID", "price": 10.0, "form": 7.5, "pts_per_match": 8.0, "total_pts": 80, "total_bonus": 15, "ict_index": 100.0, "tsb%": 60.8},
        {"id": 27, "first_name": "Riyad", "last_name": "Mahrez", "team": "Manchester City", "position": "MID", "price": 8.8, "form": 6.8, "pts_per_match": 7.5, "total_pts": 75, "total_bonus": 13, "ict_index": 95.0, "tsb%": 52.1},
        {"id": 28, "first_name": "Bernardo", "last_name": "Silva", "team": "Manchester City", "position": "MID", "price": 7.0, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 11, "ict_index": 85.0, "tsb%": 45.6},
        {"id": 29, "first_name": "Rodri", "last_name": "Hernández", "team": "Manchester City", "position": "MID", "price": 6.0, "form": 5.5, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 9, "ict_index": 80.0, "tsb%": 40.3},
        {"id": 30, "first_name": "Declan", "last_name": "Rice", "team": "Arsenal", "position": "MID", "price": 5.5, "form": 5.0, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 8, "ict_index": 75.0, "tsb%": 35.7},
        {"id": 31, "first_name": "Gabriel", "last_name": "Martinelli", "team": "Arsenal", "position": "FWD", "price": 8.0, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 12, "ict_index": 90.0, "tsb%": 50.2},
        {"id": 32, "first_name": "Darwin", "last_name": "Núñez", "team": "Liverpool", "position": "FWD", "price": 7.5, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 10, "ict_index": 85.0, "tsb%": 45.8},
        {"id": 33, "first_name": "Callum", "last_name": "Wilson", "team": "Newcastle", "position": "FWD", "price": 8.0, "form": 6.8, "pts_per_match": 7.2, "total_pts": 72, "total_bonus": 13, "ict_index": 92.0, "tsb%": 52.5},
        {"id": 34, "first_name": "Ollie", "last_name": "Watkins", "team": "Aston Villa", "position": "FWD", "price": 7.8, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 12, "ict_index": 90.0, "tsb%": 48.3},
        {"id": 35, "first_name": "Dominic", "last_name": "Calvert-Lewin", "team": "Everton", "position": "FWD", "price": 7.5, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 11, "ict_index": 85.0, "tsb%": 42.6},
        {"id": 36, "first_name": "Patrick", "last_name": "Bamford", "team": "Leeds", "position": "FWD", "price": 7.0, "form": 5.5, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 10, "ict_index": 80.0, "tsb%": 38.9},
        {"id": 37, "first_name": "David", "last_name": "Raya", "team": "Brentford", "position": "GKP", "price": 5.0, "form": 5.5, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 9, "ict_index": 82.0, "tsb%": 45.3},
        {"id": 38, "first_name": "Jordan", "last_name": "Pickford", "team": "Everton", "position": "GKP", "price": 4.8, "form": 5.0, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 8, "ict_index": 78.0, "tsb%": 40.1},
        {"id": 39, "first_name": "Robert", "last_name": "Sánchez", "team": "Brighton", "position": "GKP", "price": 4.5, "form": 4.5, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 7, "ict_index": 75.0, "tsb%": 35.4},
        {"id": 40, "first_name": "Emiliano", "last_name": "Martínez", "team": "Aston Villa", "position": "GKP", "price": 5.0, "form": 5.0, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 9, "ict_index": 80.0, "tsb%": 42.8},
        {"id": 41, "first_name": "Luke", "last_name": "Shaw", "team": "Manchester United", "position": "DEF", "price": 5.5, "form": 5.5, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 10, "ict_index": 82.0, "tsb%": 40.5},
        {"id": 42, "first_name": "John", "last_name": "Stones", "team": "Manchester City", "position": "DEF", "price": 5.8, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 11, "ict_index": 85.0, "tsb%": 45.2},
        {"id": 43, "first_name": "Ruben", "last_name": "Dias", "team": "Manchester City", "position": "DEF", "price": 6.0, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 12, "ict_index": 90.0, "tsb%": 48.9},
        {"id": 44, "first_name": "William", "last_name": "Saliba", "team": "Arsenal", "position": "DEF", "price": 5.5, "form": 5.0, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 9, "ict_index": 78.0, "tsb%": 42.3},
        {"id": 45, "first_name": "Thiago", "last_name": "Silva", "team": "Chelsea", "position": "DEF", "price": 5.0, "form": 4.5, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 8, "ict_index": 75.0, "tsb%": 38.6},
        {"id": 46, "first_name": "Ben", "last_name": "Chilwell", "team": "Chelsea", "position": "DEF", "price": 6.0, "form": 6.0, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 11, "ict_index": 88.0, "tsb%": 47.5},
        {"id": 47, "first_name": "Kyle", "last_name": "Walker", "team": "Manchester City", "position": "DEF", "price": 5.5, "form": 5.5, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 10, "ict_index": 82.0, "tsb%": 40.8},
        {"id": 48, "first_name": "Cristian", "last_name": "Romero", "team": "Tottenham", "position": "DEF", "price": 5.0, "form": 5.0, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 9, "ict_index": 78.0, "tsb%": 38.1},
        {"id": 49, "first_name": "Sven", "last_name": "Botman", "team": "Newcastle", "position": "DEF", "price": 4.5, "form": 4.5, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 8, "ict_index": 75.0, "tsb%": 33.5},
        {"id": 50, "first_name": "Tyrone", "last_name": "Mings", "team": "Aston Villa", "position": "DEF", "price": 4.8, "form": 5.0, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 9, "ict_index": 78.0, "tsb%": 37.2}
    ]

    return jsonify(player_data)  # Return as JSON

if __name__ == '__main__':
    app.run(debug=True)