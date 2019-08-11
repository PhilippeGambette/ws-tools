#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

urlOld="https://fr.wikisource.org/wiki/Spécial:Renommer_une_page/Page:Robert_-_Les_Voyages_de_Milord_Ceton_dans_les_sept_Planettes_-_tome_1.djvu/"
urlNew="Anonyme ou Collectif - Voyages imaginaires, songes, visions et romans cabalistiques, tome 17.djvu/"
firstPageNumber = 59
lastPageNumber = 159
# Pour renommer une sélection de numéros de page,
# décommentez la prochaine ligne de code ci-dessous et la ligne "for page in pages" 
# et commentez la ligne "for page in range(firstPageNumber,lastPageNumber+1):"
#pages = [67,68,69,70,71,80,81,82,83,84,93,94,95,96,97,98,107,108,109,110,111,112,121,122,123,124,125,126,135,136,137,138,139,140,149,150,151,152,153,154]

driver = webdriver.Firefox()
driver.get("https://fr.wikisource.org")
# Attention vous avez 15 secondes à l'ouverture du navigateur pour vous connecter à votre compte :
time.sleep(15)

for page in range(firstPageNumber,lastPageNumber+1):
#for page in pages :
      driver.get(urlOld+str(page))
      elem1 = driver.find_element_by_name("wpNewTitleMain")

      # Load the two versions of the text
      elem1.clear()
      elem1.send_keys(urlNew+str(page))

      # Rename by clicking the submit button
      submitButton = driver.find_element_by_name("wpMove")
      submitButton.click()

      time.sleep(6)
