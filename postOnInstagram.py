from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os
from random import randrange

chemin_en_plus = "botfleurinstagram/"

# Fonction permettant de récupérer un ensemble de tags prédéfinis
def getTags():
    nomFichier = chemin_en_plus+"differentsTags.txt"
    with open(nomFichier, 'r') as myFile:
        content = myFile.read()
        tableau_tags = content.split("\n")
        print("longueur : ", len(tableau_tags))

    nombre_tags = 30
    nombre_a_enlever = len(tableau_tags) - nombre_tags

    # print("tableau_tags : ", tableau_tags)
    for i in range(nombre_a_enlever):
        indice_random = randrange(0,len(tableau_tags))
        del tableau_tags[indice_random]

    nouveau_tableau_tags = []

    # On prends seulement les elements uniques
    for i in range(len(tableau_tags)):
        good = True
        for j in range(len(nouveau_tableau_tags)):
            if (tableau_tags[i] == nouveau_tableau_tags[j]):
                good = False
        if (good):
            nouveau_tableau_tags.append(tableau_tags[i])
    
    resultat_string = ' '.join(nouveau_tableau_tags)

    return resultat_string

# Fonction permettant de récupérer une citation avec son auteur
def getCitations():
    nomFichier = chemin_en_plus+"infosProverbes.json"
    with open(nomFichier, 'r') as myFile:
        monjson = json.loads(myFile.read())
        tableau_citations = monjson['proverbes']

        tableau_citations_2 = []

        for i in range(len(tableau_citations)):
            if (not(tableau_citations[i]['used'])):
                tableau_citations_2.append(tableau_citations[i])
        
        if (tableau_citations_2.count == 0):
            return "", ""

        element_valide = False
        while(not(element_valide)):
            indice_random = randrange(0,len(tableau_citations_2))
            if (not(tableau_citations_2[indice_random]['used'])):
                element_valide = True

        tableau_citations_2[indice_random]['used'] = True

    return tableau_citations_2[indice_random]['texte'] + "\n" + tableau_citations_2[indice_random]['auteur'], monjson

# Fonction permettant de récupérer le chemin d'une image enregistrée au préalable
def getImage():
    nomFichier = chemin_en_plus+"infosEnregistrement.json"
    with open(nomFichier, 'r') as myFile:
        monjson = json.loads(myFile.read())
        tableau_images = monjson['images']

        tableau_images_2 = []
        for i in range(len(tableau_images)):
            if (not(tableau_images[i]['used'])):
                tableau_images_2.append(tableau_images[i])
        
        if (tableau_images_2.count == 0):
            return "", "", "", ""

        element_valide = False
        while(not(element_valide)):
            indice_random = randrange(0,len(tableau_images_2))
            if (not(tableau_images_2[indice_random]['used'])):
                element_valide = True

        tableau_images_2[indice_random]['used'] = True

    chemin = os.path.abspath(chemin_en_plus+"images/" + tableau_images_2[indice_random]['nomImage'])

    tags_bonus = ""
    for i in range(len(tableau_images_2[indice_random]['tags'])):
        tags_bonus += "#" + tableau_images_2[indice_random]['tags'][i] + " "
    
    print("chemin : ", chemin)
    # print("tags_bonus : ", tags_bonus)

    return chemin, tags_bonus, tableau_images_2[indice_random]['source'], monjson

# Permet de poster une image sur instagram
def posterImageFleur():
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
    # Pour éviter les problèmes de coordonnées
    driver.maximize_window()

    driver.implicitly_wait(10)

    # Ouvrir la page
    driver.get(url)

    probleme = False
    # Publication image
    try:
        # On accepte les cookies
        driver.find_element(By.CLASS_NAME, "HoLwm").click()
        # On attends 2 secondes
        time.sleep(2)

        # On récupère login + password pour l'authentification
        tableau = driver.find_elements(By.CLASS_NAME, "zyHYP")
        login = tableau[0]
        login.send_keys("lucjager67@gmail.com")
        password = tableau[1]
        password.send_keys("j14EDCsTeiNlDHvIXTFq")

        # Bouton connection
        driver.find_element(By.CLASS_NAME, "CovQj").click()
    except:
        print("Probleme connection chien")
        driver.close()
        probleme = True

    if (probleme):
        return posterImageFleur()

    # On attends 5 secondes
    time.sleep(5)

    probleme = False
    try:
        driver.find_element(By.ID, "slfErrorAlert")
        driver.close()
        probleme = True
    except:
        print("Pas de probleme...")
    
    if (probleme):
        return posterImageFleur()

    # On attends 5 secondes
    time.sleep(5)

    # Si on me demande de save
    reussi = False
    max_fois = 1
    while (not(reussi)):
        try:
            driver.find_elements(By.CLASS_NAME, "sqdOP")[1].click()
            reussi = True
        except:
            max_fois -= 1
            reussi = False
            if (max_fois == 0):
                reussi = True
            print("On recommence 1 !")

    # Turn off notifications
    reussi = False
    max_fois = 1
    while (not(reussi)):
        try:
            driver.find_element(By.CLASS_NAME, "_a9_1").click()
            reussi = True
        except:
            max_fois -= 1
            reussi = False
            if (max_fois == 0):
                reussi = True
            print("On recommence 2 !")

    reussi = False
    # Publication image
    while (not(reussi)):
        try:
            # On récupère le bouton pour ajouter une publication
            tableau_elements = driver.find_elements(By.CLASS_NAME, "_ab6-")
            for i in range(len(tableau_elements)):
                if (tableau_elements[i].get_attribute("aria-label") == "Nouvelle publication"):
                    tableau_elements[i].click()

            # 0 -> ne fait rien
            # 1 -> Change la photo de profil
            # 2 -> Mets le texte dans la barred de recherche
            # 3 -> Mets l'image pour la publication -> trouvé !
            # On envoie l'image
            print("On envoie l'image")
            chemin_image, tags_bonus, source_image, mon_json_image = getImage()
            if (chemin_image == ""):
                print("Pas d'image disponible !")
                driver.close()
                return

            tableau_input = driver.find_elements(By.XPATH, "//input")
            tableau_input[3].send_keys(chemin_image)
            time.sleep(1)

            # On selectionne l'image
            driver.find_element(By.CLASS_NAME, "_aabm").click()

            time.sleep(1)
            # On clique sur next
            div_bouton_next = driver.find_element(By.CLASS_NAME, "_abaa")
            bouton_next = div_bouton_next.find_element(By.CLASS_NAME, "_acan")
            bouton_next.click()
            time.sleep(1)

            # Filters/Adjustements
            # TODO

            # On clique sur next
            div_bouton_next = driver.find_element(By.CLASS_NAME, "_abaa")
            bouton_next = div_bouton_next.find_element(By.CLASS_NAME, "_acan")
            bouton_next.click()
            time.sleep(1)

            citation, json_citations = getCitations()
            # Plus de citation valide
            if (citation == ""):
                print("Plus de citation valide !")
                driver.close()
                return 
            
            tags = getTags()
            # + " " + tags_bonus
            description = citation + "\n\n" + "Source : " + source_image + "\n\n" + tags
            print("description : ", description)
            # Permet de mettre un commentaire au post ainsi que les hashtags
            tableau_commentaire = driver.find_elements(By.CLASS_NAME, "_ablz")
            tableau_commentaire[len(tableau_commentaire)-1].send_keys(description)
            time.sleep(3)

            # On clique sur share
            div_bouton_next = driver.find_element(By.CLASS_NAME, "_abaa")
            bouton_next = div_bouton_next.find_element(By.CLASS_NAME, "_acan")
            bouton_next.click()
            time.sleep(15)
            reussi = True
        except:
            print("On recommence PUBLICATION !")
            reussi = False
            driver.close()
            break
        
    if (not(reussi)):
        return posterImageFleur()

    # Mise à jour used
    with open(chemin_en_plus+"infosEnregistrement.json", 'w') as myFile:
        myFile.write(json.dumps(mon_json_image))
    with open(chemin_en_plus+"infosProverbes.json", 'w') as myFile:
        myFile.write(json.dumps(json_citations))


# print("On attends...")
# while (True):
#     print("=========POSTER=============")
#     posterImageFleur()
#     print("=========ATTENDRE===========")

    
#     # 30-50 min
#     time.sleep(randrange(1800, 3000))


