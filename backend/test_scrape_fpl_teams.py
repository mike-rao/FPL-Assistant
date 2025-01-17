from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

# scrape_fpl_managers
driver.get("https://www.fplbot.app/")
search_query = "Cold Palmer"
try:
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
    print(data)
finally:
    driver.quit()

# scrape_fpl_team
url1 = "https://www.fplbot.app/"
url2 = "https://fplform.com/enter-fpl-team-id"
search_query = "Cold Palmer"
index = 0
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
    print(player_names)
finally:
    driver.quit()