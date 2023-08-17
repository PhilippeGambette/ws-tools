#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Paramètres :
identifiant = "l'identifiant_de_votre_compte_wikisource"
mdp = "votre_mot_de_passe_wikisource"

urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:Montreuil_-_Les_R%C3%AAves_morts,_1927_(premi%C3%A8re_%C3%A9dition).djvu/"
urlEnd = "&action=edit"
header = ""
firstPageNumber = 7
lastPageNumber = 68

# Pour océriser à partir d'une sélection de numéros de page,
# décommentez la prochaine ligne de code ci-dessous et la ligne "for page in pages" 
# et commentez la ligne "for page in range(firstPageNumber,lastPageNumber+1):"
#pages = [67,68,69,70,71,80,81,82,83,84,93,94,95,96,97,98,107,108,109,110,111,112,121,122,123,124,125,126,135,136,137,138,139,140,149,150,151,152,153,154]

driver = webdriver.Firefox()
driver.get("https://fr.wikisource.org/w/index.php?title=Sp%C3%A9cial:Connexion&returnto=Wikisource%3AAccueil")

# Wikisource account connection
time.sleep(2)
driver.execute_script("$('#wpName1').val('"+identifiant.replace("'","\'")+"');")
driver.execute_script("$('#wpPassword1').val('"+mdp.replace("'","\'")+"');")
elem1 = driver.find_element_by_css_selector('#wpLoginAttempt')
elem1.click()
      
time.sleep(4)

page = firstPageNumber

#for page in pages :
while page < lastPageNumber+1:
   print("page"+ str(page))
   #if ((page > 41) and (page < 54)) or ((page > 61) and (page < 73)) or ((page > 77) and (page < 86)) or ((page > 109) and (page < 122)) or ((page > 139) and (page < 141)) or ((page > 155) and (page < 167)) or ((page > 181) and (page < 190)) or ((page > 195) and (page < 202)) or ((page > 239) and (page < 254)) or ((page > 171) and (page < 280)) or ((page > 297) and (page < 308)) or ((page > 323) and (page < 332)) or ((page > 337) and (page < 348)) :
   if 1==1:
      print("page!"+ str(page))
      driver.get(urlBegin+str(page)+urlEnd)
      time.sleep(5)
      
      # Execute do_ocr()
      # driver.execute_script("do_ocr();");
      elem1 = driver.find_element_by_css_selector('[rel="GoogleOcr"]')
      #elem1 = driver.find_element_by_css_selector('.ext-wikisource-icon-ocr')
      elem1.click()
      
      '''if page%2 == 0:
         driver.execute_script("$('#wpHeaderTextbox').val('{{nr||{{espacé|LE VOYAGE DV ROY}}}}{{Manchette|G}}');")
      else :
         driver.execute_script("$('#wpHeaderTextbox').val('{{nr||{{espacé|PAR SON ROYAVME.}}|"+str(int((page-9)/2))+"}}{{Manchette|D}}');")
      '''
      # Correct typos
      time.sleep(4)
      elem1 = driver.find_element_by_css_selector('[rel="typo"]')
      elem1.click()
      
      #driver.execute_script("$('#wpTextbox1').val('<poem>'+$('#wpTextbox1').val().replace('by Google','').replace('Google','').replace('Digitized by','').replace('Digitized','')+'</poem>');")
      driver.execute_script("$('#wpTextbox1').val('{{Poem|\\n'+$('#wpTextbox1').val().replace('by Google','').replace('Google','').replace('Digitized by','').replace('Digitized','')+'\\n}}');")
      
      # Rename by clicking the submit button
      time.sleep(1)
      submitButton = driver.find_element_by_css_selector('#wpSave')
      submitButton.click()

   page += 1

