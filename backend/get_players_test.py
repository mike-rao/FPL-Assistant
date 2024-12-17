from scraper import setup_driver, scrape_stats, save_to_database, get_players_from_db, get_cached_players, get_db_connection
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Test Selenium setup
def test_setup_driver():
    print("Testing Selenium WebDriver setup...")
    try:
        driver = setup_driver()
        driver.get("https://fantasy.premierleague.com/statistics")
        print("WebDriver loaded successfully.")
        driver.quit()
    except Exception as e:
        print(f"WebDriver setup failed: {e}")

# Test scraping functionality
def test_scrape_stats():
    print("Testing web scraping...")
    try:
        stats = scrape_stats()
        print(f"Scraped {len(stats)} player(s):")
        pp.pprint(stats[:5])  # Print the first 5 players
    except Exception as e:
        print(f"Web scraping failed: {e}")

# Test saving to the database
def test_save_to_database():
    print("Testing database insertion...")
    sample_players = [
        {"name": "Player One", "goals": 10, "assists": 5},
        {"name": "Player Two", "goals": 8, "assists": 7}
    ]
    try:
        save_to_database(sample_players)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Database insertion failed: {e}")

# Test fetching data from the database
def test_get_players_from_db():
    print("Testing database retrieval...")
    try:
        players = get_players_from_db()
        print(f"Fetched {len(players)} player(s):")
        pp.pprint(players[:5])  # Print the first 5 players
    except Exception as e:
        print(f"Database retrieval failed: {e}")

# Test caching functionality
def test_get_cached_players():
    print("Testing caching...")
    try:
        players = get_cached_players()
        print(f"Retrieved {len(players)} player(s) from cache or scrape:")
        pp.pprint(players[:5])  # Print the first 5 players
    except Exception as e:
        print(f"Caching failed: {e}")

# Run tests
if __name__ == "__main__":
    # test_setup_driver()
    test_scrape_stats()
    # test_save_to_database()
    # test_get_players_from_db()
    # test_get_cached_players()
