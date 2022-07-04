from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

# Fichier json exemple
# {
#     "nombre": 0,
#     "images": [
#     ]
# }

# Permet d'enregistrer des images ainsi que les différentes infos dans un json
def enregistrerImages():
    # Initialisation
    url = "https://pixabay.com/fr/photos/search/flower/"
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    WINDOW_SIZE = "1080,1080"
    fichierInfos = "infosEnregistrement.json"
    nombre_image = 100

    # Configuration
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)

    driver.implicitly_wait(10)

    # Ouvrir la page
    driver.get(url)

    # Accepter les cookies
    driver.find_element(By.CLASS_NAME, "onetrust-close-btn-handler").click()
    # Attendre l'animation
    time.sleep(2)

    # =============================================================================
    # On récupère l'image + tags

    # Récupérer le nombre d'image
    with open(fichierInfos, 'r') as myFile:
        monJson = json.loads(myFile.read())
        print("monJson : ", monJson['nombre'])
    
    # Next page
    nombre_page_passee = 7
    for i in range(nombre_page_passee):
        driver.find_elements(By.CLASS_NAME, "button--1X-kp")[1].click()

    nombre_page = 10
    # Boucle sur les différentes pages récupérées
    for k in range(nombre_page):
        # Boucle sur les différentes images de la page
        for j in range(nombre_image):
            reussi = False
            while (not(reussi)):
                try:
                    # premiereImage = driver.find_element(By.CLASS_NAME, "container--3NC_b")
                    premiereImage = driver.find_element(By.CLASS_NAME, "link--h3bPW")
                    url_nouvelle_page = premiereImage.get_attribute("href")
                    source = url_nouvelle_page

                    #open tab
                    driver.execute_script("window.open('');")
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[1])

                    # Vers le nouveau onglet
                    driver.get(url_nouvelle_page)

                    # Suppression d'un élément qui gache la photo
                    driver.execute_script("document.getElementsByClassName(\"image-category\")[0].remove()")

                    # get screenshot of image
                    driver.find_element(By.CSS_SELECTOR, "picture").screenshot("images/image_"+str(monJson['nombre']+1)+".jpg")

                    # close the tab
                    driver.close()
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])

                    # On enregistre l'image avec un nom
                    # premiereImage.screenshot("images/image_"+str(monJson['nombre']+1)+".jpg")
                    reussi = True
                except:
                    reussi = False
                    print("On recommence 1 !")

            reussi = False
            while (not(reussi)):
                try:
                    tags = driver.find_element(By.CLASS_NAME, "keywordsContainer--yceZ_")
                    tableauTag = tags.find_elements(By.CSS_SELECTOR, "*")

                    lesTags = []
                    for i in range(len(tableauTag)):
                        # Permet d'obtenir un attribut, ici ce que contient l'element
                        lesTags.append(tableauTag[i].get_attribute("innerHTML"))
                        print("text : ", tableauTag[i].get_attribute("innerHTML"))
                    reussi = True
                except:
                    reussi = False
                    print("On recommence 3 !")

            # On enregistre dans un fichier json les informations de l'image
            monJson['nombre'] += 1
            monObjet = {
                "nomImage": "image_"+str(monJson['nombre'])+".jpg",
                "tags": lesTags,
                "used": False,
                "source": source
            }
            monJson['images'].append(monObjet)

            # On supprime l'image récupérée
            driver.execute_script("document.getElementsByClassName(\"container--3NC_b\")[0].remove()")
        
        # Next page
        driver.find_elements(By.CLASS_NAME, "button--1X-kp")[1].click()
        
    # On enregistre le résultat
    with open(fichierInfos, 'w') as myFile:
        myFile.write(json.dumps(monJson))

enregistrerImages()
