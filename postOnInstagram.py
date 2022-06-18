from typing import KeysView
from cv2 import log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os

# Initialisation
# =============================================================================
url = "https://www.instagram.com/"
PATH = "C:\Program Files (x86)\chromedriver.exe"
WINDOW_SIZE = "1080,1080"
# mon_image = "images/image_1.png"

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
tableau_boutons = driver.find_elements(By.CLASS_NAME, "_ab6-")
ajouter_publication = tableau_boutons[3]
ajouter_publication.click()

# elements = driver.find_elements(By.CLASS_NAME, "_aba7")
# div_selectionner = elements[1]

# 0 -> ne fait rien
# 1 -> Change la photo de profil
# 2 -> Mets le texte dans la barred de recherche
# 3 -> Mets l'image pour la publication -> trouvé !
# On envoie l'image
tableau_input = driver.find_elements(By.XPATH, "//input")
tableau_input[3].send_keys(
    os.path.abspath("images/image_24.jpg"))

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

# Permet de mettre un commentaire au post ainsi que les hashtags
driver.find_element(By.CLASS_NAME, "_ablz").send_keys("I am caption #flowers")

# On clique sur share
div_bouton_next = driver.find_element(By.CLASS_NAME, "_abaa")
bouton_next = div_bouton_next.find_element(By.CLASS_NAME, "_acan")
bouton_next.click()