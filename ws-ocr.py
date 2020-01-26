#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:Villedieu_-_M%C3%A9moires_de_la_vie_de_Henriette_Sylvie_de_Moli%C3%A8re,_1672.pdf/"
urlEnd = "&action=edit"
header = ""
firstPageNumber = 60
lastPageNumber = 92
# Pour océriser à partir d'une sélection de numéros de page,
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
      
      # Execute do_ocr()
      driver.execute_script("do_ocr();");

      # Correct typos
      time.sleep(5)
      elem1 = driver.find_element_by_css_selector('[rel="typo"]')
      elem1.click()
      
      # Rename by clicking the submit button
      time.sleep(1)
      submitButton = driver.find_element_by_css_selector('#wpSave')
      submitButton.click()

      page += 1
