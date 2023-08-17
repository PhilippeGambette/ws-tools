#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-
#import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Paramètres :
email = "l'email_de_votre_compte_archive.org"
mdp = "votre_mot_de_passe_archive.org"
firstPageNumber = 0
lastPageNumber = 400

driver = webdriver.Firefox()

# Connexion à votre compte :
#"""
driver.get("https://archive.org/account/login")
time.sleep(4)

driver.execute_script("document.querySelector('.input-email').value='"+email.replace("'","\'")+"'")
driver.execute_script("document.querySelector('.input-password').value='"+mdp.replace("'","\'")+"'")
time.sleep(1)

driver.find_element_by_css_selector(".btn-submit").click()
#"""

time.sleep(10)
driver.get("https://archive.org/details/posiesdemmedes00desb/page/n5/mode/2up")
time.sleep(4)

zoom = driver.find_element_by_css_selector('.icon-magnify.plus')
zoom.click()
zoom.click()
zoom.click()
zoom.click()
zoom.click()
      
time.sleep(17)

page = firstPageNumber

while page < lastPageNumber+1:
      print("Téléchargement des pages "+ str(page*2+1) + " et " + str(page*2+2))
      
      # Téléchargement de la page de gauche
      imageLeft = driver.find_element_by_css_selector('.BRpagecontainer:nth-child(4) .BRpageimage')#.get_attribute('src')
      #urllib.request.urlretrieve(imageLeft, "book-"+str(page*2+1)+"-left.jpg")
      with open("book-"+str(page*2+1)+".png", 'wb') as file:
           file.write(imageLeft.screenshot_as_png)
            
      # Téléchargement de la page de droite
      imageRight = driver.find_element_by_css_selector('.BRpagecontainer:nth-child(5) .BRpageimage')#.get_attribute('src')
      #urllib.request.urlretrieve(imageRight, "book-"+str(page*2+2)+"-right.jpg")
      with open("book-"+str(page*2+2)+".png", 'wb') as file:
           file.write(imageRight.screenshot_as_png)
      
      # Passage à la page suivante
      elem1 = driver.find_element_by_css_selector('.book_right')
      elem1.click()

      time.sleep(10)
      
      page += 1