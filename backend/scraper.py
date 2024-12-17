from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import redis
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Selenium setup
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--disable-gpu") 
    driver = webdriver.Chrome(options=options)
    return driver

# Scrape data
def scrape_stats():
    url = "https://fantasy.premierleague.com/statistics"
    driver = setup_driver()
    try:
        driver.get(url)
        stats = []

        cookie_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        cookie_btn.click()
        
        pages = driver.find_elements("xpath", "//div[@role='status' and @aria-live='polite']")[1].text
        total_pages = int(pages.split("of")[-1].strip()) 
        total_pages = 3   # testing
        for page in range(1,total_pages+1):
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Table-sc-ziussd-1.ElementTable-sc-1v08od9-0.iPaulP.OZmJL")))
            rows = table.find_elements(By.CLASS_NAME, "ElementTable__ElementRow-sc-1v08od9-3.kGMjuJ")
            print(f"Found {len(rows)} rows.")
            rows = rows[:3]   # testing
            
            driver.execute_script("window.scrollTo(0, 0);")
            for idx, row in enumerate(rows, start=1):
                try:
                    print(f"Processing row {idx}...")
                    info_button = row.find_element(By.CLASS_NAME, "ElementDialogButton__StyledElementDialogButton-sc-1vrzlgb-0.irVYoY")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ElementDialogButton__StyledElementDialogButton-sc-1vrzlgb-0.irVYoY")))
                    info_button.click()
                    popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "root-dialog")))
                    name = popup.find_element(By.CLASS_NAME, "styles__ElementHeading-sc-ahs9zc-5.gwmHpL").text
                    print(f"Popup for {name} opened successfully.")

                    stats.append({
                        "name": name,
                        "display_name": popup.find_element(By.CLASS_NAME, "ElementInTable__Name-sc-y9xi40-1.WjUOj").text,
                        "team": popup.find_element(By.CLASS_NAME, "styles__Club-sc-ahs9zc-6.eiknRS").text,
                        "position": popup.find_element(By.CLASS_NAME, "styles__ElementTypeLabel-sc-ahs9zc-4.kDMSIW").text,
                        "price": float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[0].text[1:-1]),
                        "form": float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[1].text),
                        "pts_per_match": float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[2].text),
                        "total_pts": int(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[4].text),
                        "total_bonus": int(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[5].text),
                        "ict_index": float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[6].text),
                        "tsb_percent": float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[7].text[:-1]),
                    })

                    popup.find_element(By.CLASS_NAME, "Dialog__CloseButton-sc-5bogmv-1.cgQMVU").click()
                    print(f"Popup for {name} closed.")

                except Exception as e:
                    print(f"Error extracting player data for row {idx}: {e}")
                    
            try:
                if page == 1:
                    next_btn = driver.find_element(By.CLASS_NAME, "PaginatorButton__Button-sc-xqlaki-0.cmSnxm")
                else:
                    next_btn = driver.find_elements(By.CLASS_NAME, "PaginatorButton__Button-sc-xqlaki-0.cmSnxm")[1]
                next_btn.click()
                print("Navigating to the next page...")
                time.sleep(2)
            except Exception as e:
                print("No next button found or unable to navigate. Message:", str(e))
                break

        print("Scraping complete.")
        return stats

    finally:
        driver.quit()


# Save data to database
def save_to_database(players):
    conn = get_db_connection()
    cur = conn.cursor()

    # Adjust database schema to match new format
    cur.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            name TEXT,
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
            player["total_bonus"], player["ict_index"], player["tsb%"]
        ))

    conn.commit()
    cur.close()
    conn.close()

# Get data from database
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
            "tsb%": float(p[11])
        }
        for p in players
    ]

# Fetch data with caching
def get_cached_players():
    cached_data = redis_client.get("players")
    if cached_data:
        return json.loads(cached_data)
    else:
        players = scrape_stats()
        save_to_database(players)
        redis_client.setex("players", 3600, json.dumps(players))  # Cache for 1 hour
        return players

