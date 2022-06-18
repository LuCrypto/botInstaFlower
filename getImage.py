from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

    # Boucle sur les différentes images de la page
    for j in range(nombre_image):
        reussi = False
        while (not(reussi)):
            try:
                premiereImage = driver.find_element(By.CLASS_NAME, "container--3NC_b")
                # On enregistre l'image avec un nom
                premiereImage.screenshot("images/image_"+str(monJson['nombre']+1)+".png")
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
            "nomImage": "image_"+str(monJson['nombre'])+".png",
            "tags": lesTags
        }
        monJson['images'].append(monObjet)
        monJson['used'] = False

        # On supprime l'image récupérée
        driver.execute_script("document.getElementsByClassName(\"container--3NC_b\")[0].remove()")
        
    # On enregistre le résultat
    with open(fichierInfos, 'w') as myFile:
        myFile.write(json.dumps(monJson))






# =============================================================================

# save_cookies = False
# cookies_path = 'valid_json_list_of_your_cookies_path.json'

# if save_cookies:
#     # 30 secondes pour se connecter manuellement
#     time.sleep(30)
#     print("ON SAUVEGARDE !")
#     # On récupère tous les cookies de la page
#     cookies_list = driver.get_cookies()

#     # On enregistre l'ensemble des cookies
#     with open(cookies_path, 'w') as file_path:
#         json.dump(cookies_list, file_path, indent=2, sort_keys=True)

#     driver.quit()

# else:
#     # On récupère nos cookies dans le fichier de sauvegarde
#     with open(cookies_path, 'r') as file_path:
#         cookies_list = json.loads(file_path.read())

#     # On ajoute les différentes cookies
#     for cookie in cookies_list:
#         # If domain is left in, then in the browser domain gets transformed to f'.{domain}'
#         cookie.pop('domain', None)
#         driver.add_cookie(cookie)

#     # Il faut refresh pour prendre en compte les cookies
#     driver.refresh()
#     driver.get("https://www.jeuxvideo.com/messages-prives/message.php?id=22370331&folder=0#last_msg")

# # 5 messages sur 7 affichés
# elementRoot = driver.find_element(By.CLASS_NAME, "pagination")
# elementRoot = elementRoot.find_element(By.CLASS_NAME, "action-left")

# print("Texte : ", elementRoot.text)

# tableau = str(elementRoot.text).split(' ')

# print("Nombre  : ", tableau[3])

# Permet d'enregistrer l'élément actuel dans une image
# element.screenshot("test.png")

# Ferme l'onglet actuel
# driver.close()

# Ferme le navigateur
# driver.quit()
