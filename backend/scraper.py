from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu") 
    driver = webdriver.Chrome(options=options)
    return driver

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
        # total_pages = 3   # limit for testing
        for page in range(1,total_pages+1):
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Table-sc-ziussd-1.ElementTable-sc-1v08od9-0.iPaulP.OZmJL")))
            rows = table.find_elements(By.CLASS_NAME, "ElementTable__ElementRow-sc-1v08od9-3.kGMjuJ")
            # rows = rows[:3]   # limit for testing
            
            driver.execute_script("window.scrollTo(0, 0);")
            for idx, row in enumerate(rows, start=1):
                try:
                    info_button = row.find_element(By.CLASS_NAME, "ElementDialogButton__StyledElementDialogButton-sc-1vrzlgb-0.irVYoY")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ElementDialogButton__StyledElementDialogButton-sc-1vrzlgb-0.irVYoY")))
                    info_button.click()
                    popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "root-dialog")))
                    name = popup.find_element(By.CLASS_NAME, "styles__ElementHeading-sc-ahs9zc-5.gwmHpL").text
                    display_name = row.find_element(By.CLASS_NAME, "ElementInTable__Name-sc-y9xi40-1.WjUOj").text

                    stats.append({
                        "name": name,
                        "display_name": display_name,
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
                print(f"Navigating to page {page+1}")
                time.sleep(2)
            except Exception as e:
                print("No next button found or unable to navigate. Message:", str(e))
                break

        print("Scraping complete.")
        return stats

    finally:
        driver.quit()
        
# Invoke-WebRequest -Method POST -Uri http://127.0.0.1:5000/scrape-and-save