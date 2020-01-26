#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import glob, os, re, sys, urllib.request

urlBegin="https://fr.wikisource.org/w/index.php?title=Page:Des_Roches_-_Les_Missives.pdf/"
urlEnd="&action=edit"

# Crée un fichier pour y compiler les poèmes
outputFile = open("Catherine_Des_Roches-Le_Ravissement_de_Proserpine-1586.xml","w",encoding="utf-8")

outputFile.writelines("""<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="Teinte/teinte.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-stylesheet type="text/xsl" href="Teinte/tei2html.xsl"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="fr">
   <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Le Ravissement de Proserpine, de Catherine Des Roches</title>
            <author key="Des Roches, Catherine (1542-1587). Autrice du texte">Des Roches, Catherine</author>
         </titleStmt>
         <publicationStmt>
            <publisher>Projet VisiAutrices, à partir du texte disponible sur Wikisource (feuille de style issue du projet Teinte principalement développé par Frédéric Glorieux : https://github.com/oeuvres/Teinte)</publisher>
            <date when="2018-05-14"/>
            <availability status="free">
               <p>In the public domain</p>
            </availability>
            <availability>
               <licence target="https://creativecommons.org/publicdomain/mark/1.0/"/>
            </availability>            
         </publicationStmt>
         <sourceDesc>
            <bibl>
               <author>Des Roches, Catherine (1542-1587). Autrice du texte</author>,
               <author>Des Roches, Madeleine (1520?-1587). Autrice du texte</author>,
               <title>Les Missives de Mesdames Des Roches de Poitiers Mère et Fille. Avec Le Ravissement De Proserpine Prins du Latin de Clodian. Et autres Imitations &#038; meslanges poëtiques</title>.
               <date>1586</date>,
               <publisher>A. L'Angelier (Paris)</publisher>.
               <idno type="Google Books">https://books.google.com/books?id=ZodfAAAAcAAJ</idno>
               <idno type="Wikisource">https://fr.wikisource.org/wiki/Le_Ravissement_de_Proserpine</idno>
            </bibl>
         </sourceDesc>
      </fileDesc>
      <profileDesc>
         <creation>
            <date when="1586">1586</date>
         </creation>
         <langUsage>
            <language ident="fr"/>
         </langUsage>
      </profileDesc>
   </teiHeader>
<text>
   <p>
""")

def traiteLigne(line,poemMode):
   line = line.replace("&amp;","&")
   line = line.replace("&lt;","<")

   # Traitement des deux points de début de ligne
   regexp = "^([:]+)([^:].*)"
   reste = line 
   res = re.search(regexp,reste,re.DOTALL)
   if res:
      if not(poemMode):
         line = "<br/>"
      else:
         line = ""
      nbAddedChar = 0
      while nbAddedChar < len(res.group(1)):
          line += "&#160;&#160;"
          nbAddedChar += 1
      line += res.group(2)
   else :
      line = reste

   # Suppression des sections
   regexp = "(.*)(<section[^>]*/>)(.*)"
   res = re.search(regexp,line,re.DOTALL)
   if res:
      line = res.group(1)+res.group(3)

   
   # Remplacement des ''...'' par <hi rend="italic">...</hi>
   line = line.replace("¤"," ")
   line = line.replace("''","¤")
   regexp = "([^¤]*)[¤]([^¤]+)[¤](.*)"
   res = re.search(regexp,line,re.DOTALL)
   while res:
      line = res.group(1)+"<hi rend=\"italic\">"+res.group(2)+"</hi>"+res.group(3)
      res = re.search(regexp,line,re.DOTALL)

   # Traitement des modèles Wikisource à 0 paramètre
   regexp = "([^{]*){{([^}|]+)}}(.*)"
   reste = line
   line = ""
   res = re.search(regexp,reste,re.DOTALL)
   while res:
      line += res.group(1)

      treated = False
      # modèle -
      if res.group(2) == "-":
         line += "----"
         treated = True
      
      # modèle e
      if res.group(2) == "e":
         line += "<sup>e</sup>"
         treated = True

      if not(treated):
         line += res.group(3)
      
      reste = res.group(3)
      res = re.search(regexp,reste,re.DOTALL)
   line += reste
   
   # Traitement des modèles Wikisource à >0 paramètre
   regexp = "^([^{]*){{([^|]+)[|](.*)}}([^}]*)$"
   while re.search(regexp,line,re.DOTALL):
      reste = line
      line = ""
      res = re.search(regexp,reste,re.DOTALL)
      while res:
         type = res.group(2)
         content = res.group(3)
         remaining = res.group(4)
         resremaining = re.search("^([^{]+)}}(.*)$",content,re.DOTALL)
         
         if resremaining:
            content = resremaining.group(1)
            remaining = resremaining.group(2)+"}}"+remaining
         
         #print("!? "+type+"-"+content+"  "+remaining)
         line += res.group(1)
      
         treated = False
         # modèle e
         if type.lower() == "e":
            line += "<sup>"+content+"</sup>"
            treated = True
            
         # titres de section
         if type.lower() == "t3" or type.lower() == "t4":
            line += "<p>&#160;</p><head>"+content+"</head>"
            treated = True
         
         # petites capitales
         if type.lower() == "sc":
            line += "<hi rend=\"small-caps\">"+content+"</hi>"
            treated = True

         # lettrines
         if type.lower() == "lettrine" or type.lower() == "lettrine2" :
            words = content.split("|")
            line += words[0]
            treated = True
            
         # correction de coquilles
         if type.lower() == "corr":
            words = content.split("|")
            line += "<choice><sic>"+words[0]+"</sic><corr>"+words[1]+"</corr></choice>"
            treated = True
         
         # suppression des numéros de vers
         if type.lower() == "numvers":
            treated = True

         # modèle tiret
         if type.lower() == "tiret":         
            line += content.replace("|","")
            treated = True
         if type.lower() == "tiret2":
            treated = True
      
         if not(treated):
            line += content
      
         reste = remaining
         res = re.search(regexp,reste,re.DOTALL)
      line += reste
   
   
   
   # Remplacement des balises <sup> et <sub> par <hi rend="sup"> et <hi rend="sub">
   regexp = "(.*)<sub>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"<hi rend=\"sub\">"+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   regexp = "(.*)</sub>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"</hi>"+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   regexp = "(.*)<sup>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"<hi rend=\"sup\">"+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   regexp = "(.*)</sup>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"</hi>"+res.group(2)
      res = re.search(regexp,line,re.DOTALL)
   
   # Remplacement des balises <center> par <head>
   regexp = "(.*)<([/]*)center>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"<"+res.group(2)+"head>"+res.group(3)
      res = re.search(regexp,line,re.DOTALL)
   
   # Remplacement de '' par <hi rend="i"></hi>
   # ...
   
   # Suppression des balises <big>
   regexp = "(.*)<[/]*big>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   # Suppression des balises <small>
   regexp = "(.*)<[/]*small>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   # Suppression des balises <nowiki>
   regexp = "(.*)<nowiki[/]*>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   # Remplacement des balises <br> par <lb>
   regexp = "(.*)<br[ /]*>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"<lb/>"+res.group(2)
      res = re.search(regexp,line,re.DOTALL)
   
   
   # Remplacement des balises <ref> par <note>
   regexp = "(.*)<ref>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"<note>"+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   regexp = "(.*)</ref>(.*)"
   res = re.search(regexp,line,re.DOTALL)
   while  res:
      line = res.group(1)+"</note>"+res.group(2)
      res = re.search(regexp,line,re.DOTALL)

   line = line.replace("&","&#038;")
   line = line.replace("&#038;#","&#")
   
   # espaces insécables
   for punct in [":",";","?","!"]:
       line = line.replace(" "+punct,"&#160;"+punct)
             
   return line



   
# Pour toutes les pages entre 107 et 135 :
for i in range(91,142):
   previousLineEmpty = False
   print("Page "+str(i))
   
   # Insertion de la balise indiquant le début de page et donnant l'URL du fac-similé
   outputFile.writelines("\n<pb n=\""+str(i)+"\" facs=\"https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Des_Roches_-_Les_Missives.pdf/page"+str(i)+"-960px-Des_Roches_-_Les_Missives.pdf.jpg\"/>\n")
   
   
   # Récupère la page de Wikisource en l'enregistrant dans le même dossier
   """
   with urllib.request.urlopen(urlBegin+str(i)+urlEnd) as response, open(str(i)+".html", 'wb') as out_file:
      data = response.read() # a `bytes` object
      out_file.write(data)
   """
   
   # Ouvre la page récupérée pour en extraire le poème
   lines = open(str(i)+".html","r",encoding="utf-8").readlines()
   
   # Recherche le textarea dans le fichier pour récupérer son contenu
   textareaFound = False
   poemFound = False
   for line in lines:
         
      correctedLine = ""
      if textareaFound:
         # Si on est en train de récupérer le contenu du textarea
         res = re.search("</textarea>",line)
         if res:
            # On a trouvé la fin du textarea
            textareaFound = False
         else:
            # Pas encore trouvé la fin du textarea : on enregistre la ligne
            correctedLine = line
            #print(correctedLine)
      else:
         # On cherche si la ligne contient le début du textarea
         res = re.search("<textarea[^>]*>([^<]*)$",line)
         if res:
            # On enregistre le début du textarea
            #print("Found textarea!")
            textareaFound = True
            correctedLine = res.group(1)
            #print(correctedLine)
         else:   
            res = re.search("<textarea[^>]*>(.*)</textarea>",line)
            if res:
               textareaFound = False
               correctedLine = res.group(1)

         
      if len(correctedLine)>0:
         if correctedLine == "\n":
            previousLineEmpty = True
         else:
            if previousLineEmpty:
               outputFile.writelines("&#160;</p><p>")
               previousLineEmpty = False
         saveLine = False

         """
         # Vérifie si la balise <poem> est présente :
         res = re.search("&lt;poem[^>]*>(.*)",line)
         if res:
            poemFound = True
            poemJustFound = True
         else:
            poemJustFound = False
         """

         poemStartFound = False
         poemEndFound = False         
         # Recherche la balise <poem>
         if poemFound:
            res = re.search("(.*)&lt;/poem>",correctedLine,re.DOTALL)
            if res:
               correctedLine = res.group(1)
               poemEndFound = True
               poemFound = False
            else:
               saveLine = True

         res = re.search("&lt;poem[^>]*>(.*)",correctedLine,re.DOTALL)
         if res:
            correctedLine = res.group(1)
            poemStartFound = True
            poemFound = True


         correctedLine = traiteLigne(correctedLine,poemFound)
         saveLine = True
         
         if poemFound and not((poemStartFound) and len(correctedLine)==1):
            correctedLine = "<l>"+correctedLine+"</l>"
         
         if poemEndFound and len(correctedLine)>1:
               correctedLine = "<l>"+correctedLine+"</l>"
                              
         # Traite la ligne s'il faut la sauvegarder                     
         if saveLine:
            outputFile.writelines(correctedLine)


   #outputFile.writelines("\n</page>")
outputFile.writelines("\n   </p>\n</text>")
outputFile.writelines("\n</TEI>")