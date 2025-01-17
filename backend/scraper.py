from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
        
        file = open("fpl_player_data.csv", "w", encoding="utf-8")
        file.write("player,week,position,form,pts_per_match,total_pts,total_bonus,ict_index,tsb_percent,fdr,pts_scored\n")

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
                    position = popup.find_element(By.CLASS_NAME, "styles__ElementTypeLabel-sc-ahs9zc-4.kDMSIW").text
                    form = float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[1].text)
                    pts_per_match = float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[2].text)
                    total_pts = int(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[4].text)
                    total_bonus = int(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[5].text)
                    ict_index = float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[6].text)
                    tsb_percent = float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[7].text[:-1])
                    fdr = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", "//*[starts-with(@class, 'FixtureDifficulty__StyledFixtureDifficulty')]"))).text)

                    stats.append({
                        "name": name,
                        "display_name": display_name,
                        "team": popup.find_element(By.CLASS_NAME, "styles__Club-sc-ahs9zc-6.eiknRS").text,
                        "position": position,
                        "price": float(popup.find_elements(By.CLASS_NAME, "styles__StatValue-sc-1tsp201-2.fgGEXH")[0].text[1:-1]),
                        "form": form,
                        "pts_per_match": pts_per_match,
                        "total_pts": total_pts,
                        "total_bonus": total_bonus,
                        "ict_index": ict_index,
                        "tsb_percent": tsb_percent,
                        "fdr": fdr
                    })
                    
                    week = popup.find_elements(By.CLASS_NAME, "ElementMatchGroup__MatchEvent-sc-1g84hxt-6.udNKS")[3].text
                    pts_scored = popup.find_elements(By.CLASS_NAME, "ElementMatchGroup__HistoryPts-sc-1g84hxt-8.fKkKKe")[2].text
                    
                    def get_digits(string):
                        num = ""
                        for letter in string:
                            if letter.isdigit():
                                num += letter
                        return num
                    
                    week = get_digits(week)
                    pts_scored = get_digits(pts_scored)
                    position_mapping = {"Goalkeeper": 1,"Defender": 2,"Midfielder": 3,"Forward": 4}
                    position = position_mapping.get(position)
                    
                    file.write(display_name+","+week+","+str(position)+","+str(form)+","+str(pts_per_match)+","+str(total_pts)+","+str(total_bonus)+","+str(ict_index)+","+str(tsb_percent)+","+str(fdr)+","+pts_scored+"\n")

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
        file.close()
        return stats

    finally:
        driver.quit()
        
def scrape_fpl_managers(search_query):
    url = "https://www.fplbot.app/"
    driver = setup_driver()
    try:
        driver.get(url)
        
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-input")))
        search_box.clear()
        search_box.send_keys(search_query)
        search_button = driver.find_element(By.CSS_SELECTOR, "button.font-bold.rounded.shadow.hover\\:shadow-xl.transition.duration-500.py-2.px-8.text-white.hover\\:text-fpl-purple.bg-fpl-purple.hover\\:bg-fpl-green.mt-4")
        search_button.click()
        
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pt-3")))
        rows = table.find_elements(By.CLASS_NAME, "flex.border-grey-light.border.rounded-lg.p-5.mb-1.truncate.bg-white.hover\\:bg-gray-100")
        data = []
        for row in rows:
            manager_name = row.find_element(By.CLASS_NAME, "font-bold").text
            team_name = row.find_element(By.CLASS_NAME, "text-sm.hidden.sm\\:inline-block").text
            data.append([manager_name, team_name])
        return data
    finally:
        driver.quit()
        
def scrape_fpl_team(index, search_query):
    url1 = "https://www.fplbot.app/"
    url2 = "https://fplform.com/enter-fpl-team-id"
    driver = setup_driver()
    try:
        driver.get(url1)
        
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-input")))
        search_box.clear()
        search_box.send_keys(search_query)
        search_button = driver.find_element(By.CSS_SELECTOR, "button.font-bold.rounded.shadow.hover\\:shadow-xl.transition.duration-500.py-2.px-8.text-white.hover\\:text-fpl-purple.bg-fpl-purple.hover\\:bg-fpl-green.mt-4")
        search_button.click()
        
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pt-3")))
        rows = table.find_elements(By.CLASS_NAME, "flex.border-grey-light.border.rounded-lg.p-5.mb-1.truncate.bg-white.hover\\:bg-gray-100")
        selected_row = rows[index]
        link = selected_row.find_element(By.CSS_SELECTOR, "a.underline")
        url = link.get_attribute("href")
        url_elements = url.split("/")
        team_id = url_elements[4]
        
        driver.get(url2)
        input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nospinner")))
        input_box.send_keys(team_id)
        load_button = driver.find_element("xpath", "//button[@type='submit']")
        load_button.click()
        rows = driver.find_elements(By.XPATH, "//table//tr")[1:]
        player_names = []
        for row in rows:
            select_element = row.find_element(By.TAG_NAME, "select")
            select = Select(select_element)
            selected_option_text = select.first_selected_option.text
            player_name = selected_option_text.split(" (")[0]
            player_names.append(player_name)
        return(player_names)
    finally:
        driver.quit()
        
# Invoke-WebRequest -Method POST -Uri http://127.0.0.1:5000/scrape-and-save