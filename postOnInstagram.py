from numpy import true_divide
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os
from random import randrange

# Fonction permettant de récupérer un ensemble de tags prédéfinis
def getTags():
    nomFichier = "differentsTags.txt"
    with open(nomFichier, 'r') as myFile:
        content = myFile.read()
        tableau_tags = content.split("\n")
        print("longueur : ", len(tableau_tags))

    nombre_tags = randrange(20,len(tableau_tags))
    nombre_a_enlever = len(tableau_tags) - nombre_tags

    print("tableau_tags : ", tableau_tags)
    for i in range(nombre_a_enlever):
        indice_random = randrange(0,len(tableau_tags))
        del tableau_tags[indice_random]
    
    resultat_string = ' '.join(tableau_tags)
    print("resultat_string : ", resultat_string)

    return resultat_string

# Fonction permettant de récupérer une citation avec son auteur
def getCitations():
    nomFichier = "infosProverbes.json"
    with open(nomFichier, 'r') as myFile:
        monjson = json.loads(myFile.read())
        tableau_citations = monjson['proverbes']

        element_valide = False
        while(not(element_valide)):
            indice_random = randrange(0,len(tableau_citations))
            if (not(tableau_citations[indice_random]['used'])):
                element_valide = True

        tableau_citations[indice_random]['used'] = True
    
    # Mise à jour used
    with open(nomFichier, 'w') as myFile:
        myFile.write(json.dumps(tableau_citations))

    return tableau_citations[indice_random]['texte'] + "\n" + tableau_citations[indice_random]['auteur']

# Fonction permettant de récupérer le chemin d'une image enregistrée au préalable
def getImage():
    nomFichier = "infosEnregistrement.json"
    with open(nomFichier, 'r') as myFile:
        monjson = json.loads(myFile.read())
        tableau_images = monjson['images']

        element_valide = False
        while(not(element_valide)):
            indice_random = randrange(0,len(tableau_images))
            if (not(tableau_images[indice_random]['used'])):
                element_valide = True

        tableau_images[indice_random]['used'] = True
    
    # Mise à jour used
    with open(nomFichier, 'w') as myFile:
        myFile.write(json.dumps(monjson))

    chemin = os.path.abspath("images/" + tableau_images[indice_random]['nomImage'])

    tags_bonus = ""
    for i in range(len(tableau_images[indice_random]['tags'])):
        tags_bonus += "#" + tableau_images[indice_random]['tags'][i] + " "
    
    print("chemin : ", chemin)
    print("tags_bonus : ", tags_bonus)

    return chemin, tags_bonus, tableau_images[indice_random]['source']

# Permet de poster une image sur instagram
def posterImage():
    # Initialisation
    # =============================================================================
    url = "https://www.instagram.com/"
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    WINDOW_SIZE = "1080,1080"

    # =============================================================================
    # Configuration
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=chrome_options)

    driver.implicitly_wait(10)

    # Ouvrir la page
    driver.get(url)

    # On accepte les cookies
    driver.find_element(By.CLASS_NAME, "HoLwm").click()

    # On récupère login + password pour l'authentification
    tableau = driver.find_elements(By.CLASS_NAME, "zyHYP")
    login = tableau[0]
    login.send_keys("lucjager67@gmail.com")
    password = tableau[1]
    password.send_keys("j14EDCsTeiNlDHvIXTFq")

    # Bouton connection
    driver.find_element(By.CLASS_NAME, "CovQj").click()

    # On attends 10 secondes
    time.sleep(10)

    # Turn off notifications
    driver.find_element(By.CLASS_NAME, "_a9_1").click()

    # On récupère le bouton pour ajouter une publication
    driver.find_elements(By.CLASS_NAME, "_ab6-")[3].click()

    # 0 -> ne fait rien
    # 1 -> Change la photo de profil
    # 2 -> Mets le texte dans la barred de recherche
    # 3 -> Mets l'image pour la publication -> trouvé !
    # On envoie l'image
    chemin_image, tags_bonus, source_image = getImage()
    tableau_input = driver.find_elements(By.XPATH, "//input")
    tableau_input[3].send_keys(chemin_image)

    # On clique sur next
    div_bouton_next = driver.find_element(By.CLASS_NAME, "_abaa")
    bouton_next = div_bouton_next.find_element(By.CLASS_NAME, "_acan")
    bouton_next.click()

    # Filters/Adjustements
    # TODO

    # On clique sur next
    div_bouton_next = driver.find_element(By.CLASS_NAME, "_abaa")
    bouton_next = div_bouton_next.find_element(By.CLASS_NAME, "_acan")
    bouton_next.click()

    citation = getCitations()
    tags = getTags()
    description = citation + "\n\n" + "Source : " + source_image + "\n\n" + tags + " " + tags_bonus
    # Permet de mettre un commentaire au post ainsi que les hashtags
    driver.find_element(By.CLASS_NAME, "_ablz").send_keys(description)

    # On clique sur share
    div_bouton_next = driver.find_element(By.CLASS_NAME, "_abaa")
    bouton_next = div_bouton_next.find_element(By.CLASS_NAME, "_acan")
    bouton_next.click()
    time.sleep(15)

while (True):
    posterImage()
    # 30 min
    time.sleep(1800)


