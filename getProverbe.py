from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

# Initialisation
url = "https://citations.ouest-france.fr/theme/fleur/"
PATH = "C:\Program Files (x86)\chromedriver.exe"
WINDOW_SIZE = "1080,1080"
nombre_image = 100
fichierInfos = "infosProverbes.json"

# Configuration
chrome_options = Options()
# chrome_options.add_argument("--headless")

chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)

driver.implicitly_wait(10)

# Ouvrir la page
driver.get(url)

# On récupère le json
with open(fichierInfos, 'r') as myFile:
    monJson = json.loads(myFile.read())

# =============================================================================

nombre_page = 11
for j in range(nombre_page):
    proverbes = driver.find_elements(By.CLASS_NAME, "sit")

    for i in range(len(proverbes)):
        blockquote = proverbes[i].find_element(By.CSS_SELECTOR, "blockquote")
        blockquote = blockquote.find_element(By.CSS_SELECTOR, "a")

        nombre = proverbes[i].find_elements(By.CSS_SELECTOR, "span")

        if (len(nombre) == 2):
            span = proverbes[i].find_element(By.CSS_SELECTOR, "span")
            auteur = span.get_attribute("innerHTML")
        else:
            html_a = proverbes[i].find_elements(By.CSS_SELECTOR, "a")
            auteur = html_a[1].get_attribute("innerHTML")

        print("nombre : ", len(nombre))
        print("taille : ", blockquote.get_attribute("innerHTML"))
        print("taille : ", auteur)

        # Save in json
        monObjet = {
            "texte": blockquote.get_attribute("innerHTML"),
            "auteur":  auteur,
            "used": False
        }
        monJson['proverbes'].append(monObjet)
    
    # On passe à la page suivante
    element_nav = driver.find_element(By.CLASS_NAME, "filter")
    tableau_pages = element_nav.find_elements(By.CSS_SELECTOR, "li")
    try:
        nouvelle_page = tableau_pages[j+1].find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    except:
        break
    driver.get(nouvelle_page)

# =============================================================================

# On enregistre le résultat
with open(fichierInfos, 'w') as myFile:
    myFile.write(json.dumps(monJson))

print("====================FIN")
print("Nombre proverbes : ", len(monJson['proverbes']))