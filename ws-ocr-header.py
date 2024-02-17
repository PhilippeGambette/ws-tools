#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Paramètres :
identifiant = "login"
mdp = "mdp"


urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:Marguerite_de_Navarre_-_Marguerites_de_la_Marguerite_des_princesses,_tres_illustre_royne_de_Navarre,_tome_1_(1547).pdf/"
urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:Annales_de_la_soci%C3%A9t%C3%A9_acad%C3%A9mique_de_Nantes_et_de_la_Loire-Inf%C3%A9rieure,_1907.pdf/"
urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:Gournay_-_Les_advis_ou_Les_pr%C3%A9sens_de_la_demoiselle_de_Gournay_(1641).pdf/"
urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:Desbordes-Valmore_-_Po%C3%A9sies_in%C3%A9dites,_1873.pdf/"
urlBegin = "https://fr.wikisource.org/w/index.php?title=Page:Isaac_Newton_-_Principes_math%C3%A9matiques_de_la_philosophie_naturelle,_tome2_(1759).djvu/"

urlEnd = "&action=edit"
header = ""
firstPageNumber = 344
lastPageNumber = 357


premieresPages = ["62","64","66","68","70","72","75","76","78","79","80","82","84","87","90","92","94","97","98","100","102","104","106","108","111","116","118","120","122","126","128","130","134","138","143","144","148","150","153","154","157","158","162","166","173","174","177","178","180","183","186","188","192","196","198","200","203","204","208","215","216","220","222","224","228","231","234","236","238","242","246","250","252","249","256","259","262","265","268","270","272","276","280","282","285","290","291","292","295","296","299","300","302","303","304","305","306","307","308","310","313","314","316","318","322","325","329","332","334","338","340","342","344","349","350","354","357"]
dernieresPages = ["63","65","67","69","71","74","75","77","78","79","81","83","86","89","91","93","96","97","99","101","103","105","107","110","115","117","119","121","125","127","129","133","137","142","143","147","149","152","153","156","157","161","165","172","173","176","177","179","182","185","187","191","195","197","199","202","203","207","214","215","219","221","223","227","230","233","235","237","241","245","249","251","248","255","258","261","264","267","269","271","275","279","281","284","289","290","291","294","295","298","299","301","302","303","304","305","306","307","309","312","313","315","317","321","324","328","331","333","337","339","341","343","348","349","353","356","359"]

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
      
time.sleep(2)

page = firstPageNumber

#for page in pages :
while page < lastPageNumber+1:
   print("page"+ str(page))
   pageNb = page - 189
   #if ((page > 41) and (page < 54)) or ((page > 61) and (page < 73)) or ((page > 77) and (page < 86)) or ((page > 109) and (page < 122)) or ((page > 139) and (page < 141)) or ((page > 155) and (page < 167)) or ((page > 181) and (page < 190)) or ((page > 195) and (page < 202)) or ((page > 239) and (page < 254)) or ((page > 171) and (page < 280)) or ((page > 297) and (page < 308)) or ((page > 323) and (page < 332)) or ((page > 337) and (page < 348)) :
   if 1==1:
      print("page!"+ str(page))
      driver.get(urlBegin+str(page)+urlEnd)
      time.sleep(2)
      
      #"""!!!
      # Execute do_ocr()
      # driver.execute_script("do_ocr();");
      #elem1 = driver.find_element_by_css_selector('[rel="GoogleOcr"]')
      #!!!!elem1 = driver.find_element_by_css_selector('[title="Obtenir le texte de cette image par reconnaissance optique"]')
      #elem1 = driver.find_element_by_css_selector('.ext-wikisource-icon-ocr')
      #!!!!elem1.click()
      #!!!!time.sleep(10)
      
      #elem1 = driver.find_element_by_css_selector('[rel="GoogleOcr"]')
      #elem1 = driver.find_element_by_css_selector('[title="Obtenir le texte de cette image par reconnaissance optique"]')
      #elem1.click()
      #"""
      
      #'''
      if pageNb%2 == 0:
         #driver.execute_script("$('#wpHeaderTextbox').val('{{nr||{{espacé|LE VOYAGE DV ROY}}}}{{Manchette|G}}');")
         driver.execute_script("$('#wpHeaderTextbox').val('{{Manchette|G}}{{nr|"+str(pageNb)+"|PRINCIPES MATHÉMATIQUES}}');")
      else :
         #driver.execute_script("$('#wpHeaderTextbox').val('{{nr||{{espacé|PAR SON ROYAVME.}}|"+str(int((page-9)/2))+"}}{{Manchette|D}}');")
         driver.execute_script("$('#wpHeaderTextbox').val('{{nr||DE LA PHILOSOPHIE NATURELLE|"+str(pageNb)+"}}{{Manchette|D}}');")
      #'''
      
      
      # Correct typos
      """time.sleep(7)"""
      
      """!!!
      elem1 = driver.find_element_by_css_selector('[rel="typo"]')
      elem1.click()
      time.sleep(1)
      """
      
      """
      suffixe = "ss"
      if str(page) in premieresPages:
          print("Première page !")
          suffixe = "ds"
      if str(page) in dernieresPages:
          print("Dernière page !")
          suffixe = "sf"
      if str(page) in premieresPages and str(page) in dernieresPages:
          print("Première et dernière page !")
          suffixe = "df"
      """

      #driver.execute_script("$('#wpTextbox1').val('<poem><i>'+$('#wpTextbox1').val().replace('by Google','').replace('Google','').replace('Digitized by','').replace('Digitized','')+'</i></poem>');")
      """
      if suffixe[0]=="d":
         driver.execute_script("$('#wpTextbox1').val('<nowiki/>{{brn|3}}{{t4||fs=1.5em}}{{brn|3}}{{Poem|{{sc|}}'+$('#wpTextbox1').val().replace('by Google','').replace('Google','').replace('Digitized by','').replace('Digitized','')+'\\n|"+suffixe+"}}');")
      else:
         driver.execute_script("$('#wpTextbox1').val('{{Poem|'+$('#wpTextbox1').val().replace('by Google','').replace('Google','').replace('Digitized by','').replace('Digitized','')+'\\n|"+suffixe+"}}');")
      """
      
      """
      text = driver.find_element_by_css_selector('#wpTextbox1').get_attribute("value");
      text = text.replace("'","\\'").replace("-\n","").replace("\r","\\r").replace("\n","\\n")
      time.sleep(1)
      driver.get("https://igm.univ-mlv.fr/~gambette/text-processing/fs/")
      time.sleep(1)
      #driver.find_element_by_css_selector("#textarea").set_attribute("value",text)
      #print(text)
      driver.execute_script("$('#textarea').val('"+text+"');")
      driver.find_element_by_css_selector("#nc").click()
      driver.find_element_by_css_selector('input[type="submit"]').click()
      time.sleep(8)
      text = driver.find_element_by_css_selector("#theText").get_attribute('innerText')
      driver.get(urlBegin+str(page)+urlEnd)
      #driver.find_element_by_css_selector("#wpTextbox1").set_attribute('value',text.replace("'","\'"))
      driver.execute_script("$('#wpTextbox1').val('"+text.replace("'","\'").replace(" fur "," ſur ").replace(" fa "," ſa ").replace(" fans "," ſans ").replace(" fi "," ſi ").replace("\r","\\r").replace("\n","\\n")+"');")

      #driver.execute_script("$('#wpTextbox1').val(''+$('#wpTextbox1').val().replace('by Google','').replace('Google','').replace('Digitized by','').replace('Digitized','')+'');")
      """
      driver.execute_script("$('#wpTextbox1').val(''+$('#wpTextbox1').val().replace('PRINCIPES MATHÉMATIQUES ','').replace('DE LA PHILOSOPHIE NATURELLE. ','').replace('PRINCIPES MATHÉMATIQUES','').replace('DE LA PHILOSOPHIE NATURELLE.','')+'');")
      
      
      
      # Rename by clicking the submit button
      #time.sleep(4)
      submitButton = driver.find_element_by_css_selector('#wpSave')
      submitButton.click()

   page += 1

