from selenium import webdriver # Used because requests doesn't get the full page due to javascript loading
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

chromeOptions = Options()
chromeOptions.add_argument('--ignore-certificate-errors')
chromeOptions.add_argument('--ignore-ssl-errors')
service = webdriver.ChromeService()
driver = webdriver.Chrome(service=service, options=chromeOptions)

driver.get("https://fieldsofmistria.wiki.gg/wiki/Crops")

table = driver.find_elements(By.CLASS_NAME, "wikitable.sortable.roundedborder.jquery-tablesorter")
seasons = ["SPRING", "SUMMER", "FALL", "WINTER"]
cropsDict = {"SPRING": {}, "SUMMER": {}, "FALL": {}, "WINTER": {}}
index = 0

for season in table:
    for crop in season.find_elements(By.XPATH, "tbody/tr"):
        table_elements = crop.find_elements(By.XPATH, 'td')
        (image, name, seed, source, description, period, price) = (0, 1, 2, 3, 4, 5, 6)
        name = table_elements[name].text
        cropsDict[seasons[index]][name] = {}
        cropsDict[seasons[index]][name]["Image"]       = table_elements[image].find_element(By.XPATH, 'a/img').get_attribute("src")
        cropsDict[seasons[index]][name]["Seed"]        = table_elements[seed].find_element(By.XPATH, 'a').get_attribute("title")
        
        sourcesHtml = table_elements[source].text.split("\n")
        sources = []
        for entry in sourcesHtml:
            if entry.startswith('('):
                sources[-1] += f' {entry}'
            else:
                sources.append(entry)
        cropsDict[seasons[index]][name]["Source"]      = sources

        cropsDict[seasons[index]][name]["Description"] = table_elements[description].text
        cropsDict[seasons[index]][name]["Period"]      = table_elements[period].text
        cropsDict[seasons[index]][name]["Price"]       = table_elements[price].text
    index += 1

with open("crops.json", "w") as f: 
    json.dump(cropsDict, f)

driver.close()
