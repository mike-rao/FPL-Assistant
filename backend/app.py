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
        {"id": 4, "first_name": "Kevin", "second_name": "De Bruyne", "team": "Manchester City", "element_type": "MID", "now_cost": 11.5, "total_points": 80},
        {"id": 5, "first_name": "Marcus", "second_name": "Rashford", "team": "Manchester United", "element_type": "MID", "now_cost": 9.5, "total_points": 75},
        {"id": 6, "first_name": "Trent", "second_name": "Alexander-Arnold", "team": "Liverpool", "element_type": "DEF", "now_cost": 7.5, "total_points": 70},
        {"id": 7, "first_name": "Nick", "second_name": "Pope", "team": "Newcastle", "element_type": "GK", "now_cost": 5.5, "total_points": 65},
        {"id": 8, "first_name": "Bukayo", "second_name": "Saka", "team": "Arsenal", "element_type": "MID", "now_cost": 8.2, "total_points": 72},
        {"id": 9, "first_name": "Gabriel", "second_name": "Jesus", "team": "Arsenal", "element_type": "FWD", "now_cost": 8.0, "total_points": 68},
        {"id": 10, "first_name": "James", "second_name": "Ward-Prowse", "team": "West Ham", "element_type": "MID", "now_cost": 6.5, "total_points": 65},
        {"id": 11, "first_name": "Son", "second_name": "Heung-Min", "team": "Tottenham", "element_type": "MID", "now_cost": 9.8, "total_points": 82},
        {"id": 12, "first_name": "Alexander", "second_name": "Isak", "team": "Newcastle", "element_type": "FWD", "now_cost": 7.8, "total_points": 62},
        {"id": 13, "first_name": "Kieran", "second_name": "Trippier", "team": "Newcastle", "element_type": "DEF", "now_cost": 6.8, "total_points": 78},
        {"id": 14, "first_name": "Alisson", "second_name": "Becker", "team": "Liverpool", "element_type": "GK", "now_cost": 5.4, "total_points": 64},
        {"id": 15, "first_name": "Martin", "second_name": "Ødegaard", "team": "Arsenal", "element_type": "MID", "now_cost": 7.5, "total_points": 70},
        {"id": 16, "first_name": "Ivan", "second_name": "Toney", "team": "Brentford", "element_type": "FWD", "now_cost": 7.0, "total_points": 66},
        {"id": 17, "first_name": "Virgil", "second_name": "van Dijk", "team": "Liverpool", "element_type": "DEF", "now_cost": 6.3, "total_points": 60},
        {"id": 18, "first_name": "Aaron", "second_name": "Ramsdale", "team": "Arsenal", "element_type": "GK", "now_cost": 5.2, "total_points": 60},
        {"id": 19, "first_name": "Phil", "second_name": "Foden", "team": "Manchester City", "element_type": "MID", "now_cost": 7.2, "total_points": 68},
        {"id": 20, "first_name": "Raheem", "second_name": "Sterling", "team": "Chelsea", "element_type": "MID", "now_cost": 7.5, "total_points": 62},
        {"id": 21, "first_name": "Bruno", "second_name": "Fernandes", "team": "Manchester United", "element_type": "MID", "now_cost": 8.5, "total_points": 70},
        {"id": 22, "first_name": "Kai", "second_name": "Havertz", "team": "Arsenal", "element_type": "MID", "now_cost": 6.0, "total_points": 55},
        {"id": 23, "first_name": "Reece", "second_name": "James", "team": "Chelsea", "element_type": "DEF", "now_cost": 5.5, "total_points": 50},
        {"id": 24, "first_name": "Ederson", "second_name": "Moraes", "team": "Manchester City", "element_type": "GK", "now_cost": 5.6, "total_points": 65},
        {"id": 25, "first_name": "Callum", "second_name": "Wilson", "team": "Newcastle", "element_type": "FWD", "now_cost": 6.7, "total_points": 58},
        {"id": 26, "first_name": "Luis", "second_name": "Diaz", "team": "Liverpool", "element_type": "MID", "now_cost": 7.3, "total_points": 62},
        {"id": 27, "first_name": "Anthony", "second_name": "Gordon", "team": "Newcastle", "element_type": "MID", "now_cost": 5.9, "total_points": 52},
        {"id": 28, "first_name": "Dominic", "second_name": "Calvert-Lewin", "team": "Everton", "element_type": "FWD", "now_cost": 6.3, "total_points": 50},
        {"id": 29, "first_name": "Joao", "second_name": "Palhinha", "team": "Fulham", "element_type": "MID", "now_cost": 5.5, "total_points": 45},
        {"id": 30, "first_name": "Danny", "second_name": "Ings", "team": "West Ham", "element_type": "FWD", "now_cost": 6.0, "total_points": 45},
        {"id": 31, "first_name": "Jason", "second_name": "Steele", "team": "Brighton", "element_type": "GK", "now_cost": 4.5, "total_points": 55},
        {"id": 32, "first_name": "Solly", "second_name": "March", "team": "Brighton", "element_type": "MID", "now_cost": 6.0, "total_points": 58},
        {"id": 33, "first_name": "Eberechi", "second_name": "Eze", "team": "Crystal Palace", "element_type": "MID", "now_cost": 6.3, "total_points": 53},
        {"id": 34, "first_name": "Ben", "second_name": "Chilwell", "team": "Chelsea", "element_type": "DEF", "now_cost": 5.8, "total_points": 55},
        {"id": 35, "first_name": "Wilfried", "second_name": "Gnonto", "team": "Leeds", "element_type": "FWD", "now_cost": 5.5, "total_points": 45},
        {"id": 36, "first_name": "Emiliano", "second_name": "Buendia", "team": "Aston Villa", "element_type": "MID", "now_cost": 5.9, "total_points": 50},
        {"id": 37, "first_name": "Tyrone", "second_name": "Mings", "team": "Aston Villa", "element_type": "DEF", "now_cost": 5.1, "total_points": 52},
        {"id": 38, "first_name": "Emiliano", "second_name": "Martinez", "team": "Aston Villa", "element_type": "GK", "now_cost": 5.5, "total_points": 58},
        {"id": 39, "first_name": "Lucas", "second_name": "Digne", "team": "Aston Villa", "element_type": "DEF", "now_cost": 5.0, "total_points": 50},
        {"id": 40, "first_name": "Douglas", "second_name": "Luiz", "team": "Aston Villa", "element_type": "MID", "now_cost": 5.5, "total_points": 48},
        {"id": 41, "first_name": "Joelinton", "second_name": "", "team": "Newcastle", "element_type": "MID", "now_cost": 5.9, "total_points": 55},
        {"id": 42, "first_name": "Mohamed", "second_name": "Elneny", "team": "Arsenal", "element_type": "MID", "now_cost": 4.8, "total_points": 40},
        {"id": 43, "first_name": "Pascal", "second_name": "Gross", "team": "Brighton", "element_type": "MID", "now_cost": 6.5, "total_points": 60},
        {"id": 44, "first_name": "Rico", "second_name": "Henry", "team": "Brentford", "element_type": "DEF", "now_cost": 4.5, "total_points": 42},
        {"id": 45, "first_name": "James", "second_name": "Tarkowski", "team": "Everton", "element_type": "DEF", "now_cost": 4.4, "total_points": 45},
        {"id": 46, "first_name": "Jordan", "second_name": "Pickford", "team": "Everton", "element_type": "GK", "now_cost": 4.8, "total_points": 50},
        {"id": 47, "first_name": "Andreas", "second_name": "Pereira", "team": "Fulham", "element_type": "MID", "now_cost": 4.5, "total_points": 48},
        {"id": 48, "first_name": "Aleksandar", "second_name": "Mitrovic", "team": "Fulham", "element_type": "FWD", "now_cost": 7.0, "total_points": 60},
        {"id": 49, "first_name": "Marc", "second_name": "Cucurella", "team": "Chelsea", "element_type": "DEF", "now_cost": 5.0, "total_points": 46},
        {"id": 50, "first_name": "Pierre-Emile", "second_name": "Højbjerg", "team": "Tottenham", "element_type": "MID", "now_cost": 5.0, "total_points": 44},
    ]

    return jsonify(player_data)  # Return as JSON

if __name__ == '__main__':
    app.run(debug=True)