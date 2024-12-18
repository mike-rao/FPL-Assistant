import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def initialize_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE,
            display_name TEXT,
            team TEXT,
            position TEXT,
            price NUMERIC,
            form NUMERIC,
            pts_per_match NUMERIC,
            total_pts INTEGER,
            total_bonus INTEGER,
            ict_index NUMERIC,
            tsb_percent NUMERIC
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized.")

def save_to_database(players):
    conn = get_db_connection()
    cur = conn.cursor()
    for player in players:
        cur.execute('''
            INSERT INTO players (
                name, display_name, team, position, price, form, pts_per_match, 
                total_pts, total_bonus, ict_index, tsb_percent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                team = EXCLUDED.team,
                position = EXCLUDED.position,
                price = EXCLUDED.price,
                form = EXCLUDED.form,
                pts_per_match = EXCLUDED.pts_per_match,
                total_pts = EXCLUDED.total_pts,
                total_bonus = EXCLUDED.total_bonus,
                ict_index = EXCLUDED.ict_index,
                tsb_percent = EXCLUDED.tsb_percent
        ''', (
            player["name"], player["display_name"], player["team"], player["position"],
            player["price"], player["form"], player["pts_per_match"], player["total_pts"],
            player["total_bonus"], player["ict_index"], player["tsb_percent"]
        ))
    conn.commit()
    cur.close()
    conn.close()
    print("Saved to database.")

def get_players_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM players')
    players = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": p[0],
            "name": p[1],
            "display_name": p[2],
            "team": p[3],
            "position": p[4],
            "price": float(p[5]),
            "form": float(p[6]),
            "pts_per_match": float(p[7]),
            "total_pts": int(p[8]),
            "total_bonus": int(p[9]),
            "ict_index": float(p[10]),
            "tsb_percent": float(p[11])
        }
        for p in players
    ]

def clear_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM players;")
    conn.commit()
    cur.close()
    conn.close()
    print("Table cleared.")