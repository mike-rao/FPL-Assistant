from scraper import setup_driver, scrape_stats
from database import save_to_database, get_players_from_db, initialize_database, clear_table
import pprint

pp = pprint.PrettyPrinter(indent=4)

def test_setup_driver():
    print("Testing Selenium WebDriver setup...")
    try:
        driver = setup_driver()
        driver.get("https://fantasy.premierleague.com/statistics")
        print("WebDriver loaded successfully.")
        driver.quit()
    except Exception as e:
        print(f"WebDriver setup failed: {e}")

def test_scrape_stats():
    print("Testing web scraping...")
    try:
        stats = scrape_stats()
        print(f"Scraped {len(stats)} player(s):")
        pp.pprint(stats[:5])
    except Exception as e:
        print(f"Web scraping failed: {e}")

def test_save_to_database():
    print("Testing database insertion...")
    sample_players = [
        {'name': 'Mohamed Salah', 'display_name': 'M.Salah', 'team': 'Liverpool', 'position': 'Midfielder', 'price': 13.4, 'form': 12.2, 'pts_per_match': 10.4, 'total_pts': 156, 'total_bonus': 28, 'ict_index': 188.1, 'tsb_percent': 63.4, 'fdr': 4}, 
        {'name': 'Cole Palmer', 'display_name': 'Palmer', 'team': 'Chelsea', 'position': 'Midfielder', 'price': 11.2, 'form': 8.8, 'pts_per_match': 8.0, 'total_pts': 128, 'total_bonus': 20, 'ict_index': 178.3, 'tsb_percent': 63.4, 'fdr': 2},        
        {'name': 'Bukayo Saka', 'display_name': 'Saka', 'team': 'Arsenal', 'position': 'Midfielder', 'price': 10.6, 'form': 7.8, 'pts_per_match': 7.1, 'total_pts': 106, 'total_bonus': 16, 'ict_index': 174.9, 'tsb_percent': 44.4, 'fdr': 2}
    ]
    try:
        save_to_database(sample_players)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Database insertion failed: {e}")

def test_get_players_from_db():
    print("Testing database retrieval...")
    try:
        players = get_players_from_db()
        print(f"Fetched {len(players)} player(s):")
        pp.pprint(players[:5])
    except Exception as e:
        print(f"Database retrieval failed: {e}")

if __name__ == "__main__":
    test_setup_driver()
    test_scrape_stats()
    initialize_database()
    test_save_to_database()
    test_get_players_from_db()
