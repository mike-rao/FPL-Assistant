from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import scrape_stats
from database import save_to_database, get_players_from_db

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

if __name__ == '__main__':
    app.run(debug=True)