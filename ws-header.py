#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:De_Th%C3%A9is_-_Oeuvres_compl%C3%A8tes,_Tome_3,_1842.djvu/"
urlEnd = "&action=edit"
header = ""
firstPageNumber = 24
lastPageNumber = 146
headerBegin="{{nr|"
headerEnd="|VINGT-QUATRE HEURES}}"
headerBegin="{{nr||D’UNE FEMME SENSIBLE.|"
headerEnd="}}"
headerPageNumber = 21
# Pour renommer une sélection de numéros de page,
# décommentez la prochaine ligne de code ci-dessous et la ligne "for page in pages" 
# et commentez la ligne "for page in range(firstPageNumber,lastPageNumber+1):"
#pages = [67,68,69,70,71,80,81,82,83,84,93,94,95,96,97,98,107,108,109,110,111,112,121,122,123,124,125,126,135,136,137,138,139,140,149,150,151,152,153,154]

driver = webdriver.Firefox()
driver.get("https://fr.wikisource.org")
# Attention vous avez 15 secondes à l'ouverture du navigateur pour vous connecter à votre compte :
time.sleep(15)

page = firstPageNumber

while page < lastPageNumber+1:
#for page in pages :
      driver.get(urlBegin+str(page)+urlEnd)
      time.sleep(2)
      
      # Click the button to display the header
      if page == firstPageNumber:
         elem1 = driver.find_element_by_css_selector('[aria-controls="wikiEditor-section-proofreadpage-tools"]')
         elem1.click()
         time.sleep(2)
      
      elem1 = driver.find_element_by_css_selector('[title="Afficher/cacher l’en-tête et le pied de page de cette page"]')
      elem1.click()
      time.sleep(1)

      # Select the header and change it
      elem1 = driver.find_element_by_css_selector('#wpHeaderTextbox')      
      elem1.send_keys(headerBegin+str(headerPageNumber)+headerEnd)

      # Rename by clicking the submit button
      submitButton = driver.find_element_by_css_selector('#wpSave')
      submitButton.click()

      headerPageNumber += 2
      page += 2
      time.sleep(4)
