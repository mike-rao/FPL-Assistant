from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import get_cached_players, get_players_from_db

app = Flask(__name__)
CORS(app)

# Route to fetch player data
@app.route('/players', methods=['GET'])
def get_players():
    try:
        # Fetch players from cache or scrape as needed
        players = get_cached_players()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(players)

# Route to fetch player data from database
@app.route('/players/db', methods=['GET'])
def get_players_from_database():
    try:
        players = get_players_from_db()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(players)

@app.route('/get_player_data', methods=['GET'])
def get_player_data():
    player_data = [
        {"id": 1, "first_name": "Alisson", "last_name": "Becker", "team": "Liverpool", "position": "GKP", "price": 5.5, "form": 6.0, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 10, "ict_index": 82.0, "tsb%": 48.0},
        {"id": 2, "first_name": "Aaron", "last_name": "Ramsdale", "team": "Arsenal", "position": "GKP", "price": 5.0, "form": 5.5, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 8, "ict_index": 78.0, "tsb%": 42.0},
        {"id": 3, "first_name": "Trent", "last_name": "Alexander-Arnold", "team": "Liverpool", "position": "DEF", "price": 7.0, "form": 7.0, "pts_per_match": 7.2, "total_pts": 72, "total_bonus": 12, "ict_index": 92.0, "tsb%": 58.0},
        {"id": 4, "first_name": "Kieran", "last_name": "Trippier", "team": "Newcastle", "position": "DEF", "price": 6.5, "form": 6.5, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 10, "ict_index": 88.0, "tsb%": 52.0},
        {"id": 5, "first_name": "Reece", "last_name": "James", "team": "Chelsea", "position": "DEF", "price": 6.0, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 48.0},
        {"id": 6, "first_name": "João", "last_name": "Cancelo", "team": "Man City", "position": "DEF", "price": 6.8, "form": 6.8, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 11, "ict_index": 90.0, "tsb%": 55.0},
        {"id": 7, "first_name": "William", "last_name": "Saliba", "team": "Arsenal", "position": "DEF", "price": 5.5, "form": 5.5, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 8, "ict_index": 80.0, "tsb%": 45.0},
        {"id": 8, "first_name": "Mohamed", "last_name": "Salah", "team": "Liverpool", "position": "MID", "price": 13.0, "form": 8.5, "pts_per_match": 9.2, "total_pts": 92, "total_bonus": 18, "ict_index": 118.0, "tsb%": 72.0},
        {"id": 9, "first_name": "Kevin", "last_name": "De Bruyne", "team": "Man City", "position": "MID", "price": 12.0, "form": 8.0, "pts_per_match": 8.8, "total_pts": 88, "total_bonus": 16, "ict_index": 112.0, "tsb%": 68.0},
        {"id": 10, "first_name": "Bruno", "last_name": "Fernandes", "team": "Man Utd", "position": "MID", "price": 9.5, "form": 7.5, "pts_per_match": 8.0, "total_pts": 80, "total_bonus": 14, "ict_index": 100.0, "tsb%": 60.0},
        {"id": 11, "first_name": "Martin", "last_name": "Ødegaard", "team": "Arsenal", "position": "MID", "price": 8.5, "form": 7.0, "pts_per_match": 7.5, "total_pts": 75, "total_bonus": 12, "ict_index": 95.0, "tsb%": 55.0},
        {"id": 12, "first_name": "James", "last_name": "Maddison", "team": "Spurs", "position": "MID", "price": 8.0, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 10, "ict_index": 90.0, "tsb%": 50.0},
        {"id": 13, "first_name": "Erling", "last_name": "Haaland", "team": "Man City", "position": "FWD", "price": 14.0, "form": 9.0, "pts_per_match": 9.8, "total_pts": 98, "total_bonus": 20, "ict_index": 125.0, "tsb%": 80.0},
        {"id": 14, "first_name": "Harry", "last_name": "Kane", "team": "Spurs", "position": "FWD", "price": 12.5, "form": 8.5, "pts_per_match": 9.0, "total_pts": 90, "total_bonus": 18, "ict_index": 115.0, "tsb%": 70.0},
        {"id": 15, "first_name": "Ivan", "last_name": "Toney", "team": "Brentford", "position": "FWD", "price": 9.0, "form": 7.0, "pts_per_match": 7.8, "total_pts": 78, "total_bonus": 14, "ict_index": 100.0, "tsb%": 60.0}, 
        {"id": 16, "first_name": "Ollie", "last_name": "Watkins", "team": "Aston Villa", "position": "FWD", "price": 8.5, "form": 6.5, "pts_per_match": 7.2, "total_pts": 72, "total_bonus": 12, "ict_index": 92.0, "tsb%": 55.0},
        {"id": 17, "first_name": "Marcus", "last_name": "Rashford", "team": "Man Utd", "position": "MID", "price": 10.0, "form": 7.8, "pts_per_match": 8.2, "total_pts": 82, "total_bonus": 15, "ict_index": 105.0, "tsb%": 62.0},
        {"id": 18, "first_name": "Bukayo", "last_name": "Saka", "team": "Arsenal", "position": "MID", "price": 9.0, "form": 7.2, "pts_per_match": 7.8, "total_pts": 78, "total_bonus": 13, "ict_index": 98.0, "tsb%": 58.0},
        {"id": 19, "first_name": "Phil", "last_name": "Foden", "team": "Man City", "position": "MID", "price": 8.0, "form": 6.8, "pts_per_match": 7.2, "total_pts": 72, "total_bonus": 11, "ict_index": 92.0, "tsb%": 52.0},
        {"id": 20, "first_name": "Eberechi", "last_name": "Eze", "team": "Crystal Palace", "position": "MID", "price": 7.5, "form": 6.2, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 9, "ict_index": 88.0, "tsb%": 48.0},
        {"id": 21, "first_name": "David", "last_name": "Raya", "team": "Brentford", "position": "GKP", "price": 4.8, "form": 5.0, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 7, "ict_index": 75.0, "tsb%": 38.0},
        {"id": 22, "first_name": "Nick", "last_name": "Pope", "team": "Newcastle", "position": "GKP", "price": 5.5, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 45.0},
        {"id": 23, "first_name": "Gabriel", "last_name": "Magalhães", "team": "Arsenal", "position": "DEF", "price": 5.0, "form": 5.5, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 8, "ict_index": 82.0, "tsb%": 40.0},
        {"id": 24, "first_name": "Sven", "last_name": "Botman", "team": "Newcastle", "position": "DEF", "price": 4.5, "form": 5.0, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 7, "ict_index": 78.0, "tsb%": 35.0},
        {"id": 25, "first_name": "Lewis", "last_name": "Dunk", "team": "Brighton", "position": "DEF", "price": 4.8, "form": 5.2, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 8, "ict_index": 80.0, "tsb%": 38.0},
        {"id": 26, "first_name": "Tyrone", "last_name": "Mings", "team": "Aston Villa", "position": "DEF", "price": 5.0, "form": 5.5, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 9, "ict_index": 82.0, "tsb%": 40.0},
        {"id": 27, "first_name": "Pervis", "last_name": "Estupiñán", "team": "Brighton", "position": "DEF", "price": 5.5, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 10, "ict_index": 85.0, "tsb%": 45.0},
        {"id": 28, "first_name": "Declan", "last_name": "Rice", "team": "Arsenal", "position": "MID", "price": 6.0, "form": 5.5, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 8, "ict_index": 82.0, "tsb%": 40.0},
        {"id": 29, "first_name": "Lucas", "last_name": "Paquetá", "team": "West Ham", "position": "MID", "price": 7.0, "form": 6.0, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 10, "ict_index": 88.0, "tsb%": 48.0},
        {"id": 30, "first_name": "Youri", "last_name": "Tielemans", "team": "Aston Villa", "position": "MID", "price": 6.5, "form": 6.2, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 45.0},
        {"id": 31, "first_name": "Alexis", "last_name": "Mac Allister", "team": "Liverpool", "position": "MID", "price": 7.5, "form": 6.8, "pts_per_match": 7.2, "total_pts": 72, "total_bonus": 11, "ict_index": 92.0, "tsb%": 52.0},
        {"id": 32, "first_name": "Dominik", "last_name": "Szoboszlai", "team": "Liverpool", "position": "MID", "price": 7.0, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 10, "ict_index": 90.0, "tsb%": 50.0},
        {"id": 33, "first_name": "Alexander", "last_name": "Isak", "team": "Newcastle", "position": "FWD", "price": 8.0, "form": 6.8, "pts_per_match": 7.5, "total_pts": 75, "total_bonus": 12, "ict_index": 95.0, "tsb%": 55.0},
        {"id": 34, "first_name": "Callum", "last_name": "Wilson", "team": "Newcastle", "position": "FWD", "price": 7.5, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 11, "ict_index": 90.0, "tsb%": 50.0},
        {"id": 35, "first_name": "Gabriel", "last_name": "Jesus", "team": "Arsenal", "position": "FWD", "price": 8.5, "form": 7.0, "pts_per_match": 7.8, "total_pts": 78, "total_bonus": 13, "ict_index": 98.0, "tsb%": 58.0},
        {"id": 36, "first_name": "Evan", "last_name": "Ferguson", "team": "Brighton", "position": "FWD", "price": 6.0, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 10, "ict_index": 85.0, "tsb%": 45.0},
        {"id": 37, "first_name": "Taiwo", "last_name": "Awoniyi", "team": "Nott'm Forest", "position": "FWD", "price": 6.5, "form": 5.8, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 9, "ict_index": 82.0, "tsb%": 40.0},
        {"id": 38, "first_name": "Jarrod", "last_name": "Bowen", "team": "West Ham", "position": "MID", "price": 7.0, "form": 6.2, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 10, "ict_index": 88.0, "tsb%": 48.0},
        {"id": 39, "first_name": "Morgan", "last_name": "Gibbs-White", "team": "Nott'm Forest", "position": "MID", "price": 6.5, "form": 5.8, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 45.0},
        {"id": 40, "first_name": "Kaoru", "last_name": "Mitoma", "team": "Brighton", "position": "MID", "price": 6.8, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 10, "ict_index": 90.0, "tsb%": 50.0},
        {"id": 41, "first_name": "James", "last_name": "Ward-Prowse", "team": "West Ham", "position": "MID", "price": 6.5, "form": 5.8, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 9, "ict_index": 82.0, "tsb%": 40.0},
        {"id": 42, "first_name": "Pedro", "last_name": "Neto", "team": "Wolves", "position": "MID", "price": 6.0, "form": 5.5, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 8, "ict_index": 80.0, "tsb%": 38.0},
        {"id": 43, "first_name": "Matheus", "last_name": "Cunha", "team": "Wolves", "position": "FWD", "price": 7.0, "form": 6.2, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 10, "ict_index": 88.0, "tsb%": 48.0},
        {"id": 44, "first_name": "Pablo", "last_name": "Sarabia", "team": "Wolves", "position": "MID", "price": 6.5, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 45.0},
        {"id": 45, "first_name": "Daniel", "last_name": "Podence", "team": "Wolves", "position": "MID", "price": 5.5, "form": 5.2, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 8, "ict_index": 78.0, "tsb%": 35.0},
        {"id": 46, "first_name": "Brennan", "last_name": "Johnson", "team": "Nott'm Forest", "position": "FWD", "price": 6.0, "form": 5.5, "pts_per_match": 6.0, "total_pts": 60, "total_bonus": 7, "ict_index": 80.0, "tsb%": 38.0},
        {"id": 47, "first_name": "Che", "last_name": "Adams", "team": "Southampton", "position": "FWD", "price": 6.5, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 42.0},
        {"id": 48, "first_name": "James", "last_name": "Justin", "team": "Leicester", "position": "DEF", "price": 4.5, "form": 4.8, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 7, "ict_index": 75.0, "tsb%": 30.0},
        {"id": 49, "first_name": "Ricardo", "last_name": "Pereira", "team": "Leicester", "position": "DEF", "price": 4.8, "form": 5.0, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 8, "ict_index": 78.0, "tsb%": 35.0},
        {"id": 50, "first_name": "Wout", "last_name": "Faes", "team": "Leicester", "position": "DEF", "price": 4.5, "form": 4.5, "pts_per_match": 5.2, "total_pts": 52, "total_bonus": 6, "ict_index": 72.0, "tsb%": 28.0},
        {"id": 51, "first_name": "Harvey", "last_name": "Barnes", "team": "Leicester", "position": "MID", "price": 6.5, "form": 6.0, "pts_per_match": 6.8, "total_pts": 68, "total_bonus": 10, "ict_index": 88.0, "tsb%": 45.0},
        {"id": 52, "first_name": "Patson", "last_name": "Daka", "team": "Leicester", "position": "FWD", "price": 6.0, "form": 5.5, "pts_per_match": 6.2, "total_pts": 62, "total_bonus": 9, "ict_index": 82.0, "tsb%": 40.0},
        {"id": 53, "first_name": "Wilfried", "last_name": "Zaha", "team": "Crystal Palace", "position": "MID", "price": 7.0, "form": 6.5, "pts_per_match": 7.0, "total_pts": 70, "total_bonus": 11, "ict_index": 90.0, "tsb%": 50.0},
        {"id": 54, "first_name": "Michael", "last_name": "Olise", "team": "Crystal Palace", "position": "MID", "price": 6.5, "form": 6.2, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 10, "ict_index": 85.0, "tsb%": 45.0},
        {"id": 55, "first_name": "Joachim", "last_name": "Andersen", "team": "Crystal Palace", "position": "DEF", "price": 4.5, "form": 4.8, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 7, "ict_index": 75.0, "tsb%": 30.0},
        {"id": 56, "first_name": "Jordan", "last_name": "Ayew", "team": "Crystal Palace", "position": "FWD", "price": 5.5, "form": 5.0, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 8, "ict_index": 78.0, "tsb%": 35.0},
        {"id": 57, "first_name": "Dominic", "last_name": "Solanke", "team": "Bournemouth", "position": "FWD", "price": 6.5, "form": 6.0, "pts_per_match": 6.5, "total_pts": 65, "total_bonus": 9, "ict_index": 85.0, "tsb%": 42.0},
        {"id": 58, "first_name": "Philip", "last_name": "Billing", "team": "Bournemouth", "position": "MID", "price": 5.5, "form": 5.2, "pts_per_match": 5.8, "total_pts": 58, "total_bonus": 8, "ict_index": 78.0, "tsb%": 35.0},
        {"id": 59, "first_name": "Marcos", "last_name": "Senesi", "team": "Bournemouth", "position": "DEF", "price": 4.8, "form": 5.0, "pts_per_match": 5.5, "total_pts": 55, "total_bonus": 7, "ict_index": 75.0, "tsb%": 30.0},
        {"id": 60, "first_name": "Neto", "last_name": "", "team": "Bournemouth", "position": "GKP", "price": 4.5, "form": 4.5, "pts_per_match": 5.2, "total_pts": 52, "total_bonus": 6, "ict_index": 72.0, "tsb%": 28.0}
    ]

    return jsonify(player_data)

if __name__ == '__main__':
    app.run(debug=True)