#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-

import glob, os, re, sys, urllib.request


# == Common structure of all francophone wikisource book index page URLs ==
urlBegin="https://fr.wikisource.org/wiki/Livre:"
urlEnd=""


# == List of metadata captured on each book ==
# -ws means on Wikisource
# -wd means on Wikidata
# author may include only first author or several authors
metadata = ["author", "author-ws", "author-wd", "title", "title-ws", "title-wd", "publisher", "year", "bnf", "status"]


# == Dictionary of regular expressions to capture metadata about the books ==
regexDict = {}
regexDict["author"] = ["Auteur</th><td>([^<]*)</td>", "Auteur</th><td><span><a href=.[^\"]*. title=.[^>]*>([^<]*)</a>"]
regexDict["author-ws"] = ["Auteur</th><td><span><a href=./wiki/([^\"]*). title"]
regexDict["author-wd"] = ["Auteur</th><td><span><a href=.[^\"]*. title=.[^>]*>[^<]*</a> <a href=.https://www.wikidata.org/wiki/(Q[0-9]*). title=.Voir et modifier les données sur Wikidata.>"]
regexDict["title"] = ["Titre</th><td>([^<]*)</td>", "Titre</th><td><span><a href=.[^\"]*. title=.[^>]*>([^<]*)</a>"]
regexDict["title-ws"] = ["Titre</th><td><span><a href=./wiki/([^\"]*). title"]
regexDict["title-wd"] = ["Titre</th><td><span><a href=.[^\"]*. title=.[^>]*>[^<]*</a> <a href=.https://www.wikidata.org/wiki/(Q[0-9]*). title=.Voir et modifier les données sur Wikidata.>"]
regexDict["publisher"] = ["Maison&#160;d’édition</th><td>([^<]*)</td>", "Maison&#160;d’édition</th><td><span><a href=.[^\"]*. title=.[^>]*>([^<]*)</a>"]
regexDict["year"] = ["Année&#160;d’édition</th><td>([^<]*)</td>", "Année&#160;d’édition</th><td><span><a href=.[^\"]*. title=.[^>]*>([^<]*)</a>"]
regexDict["bnf"] = ["Bibliothèque</th><td><a rel=.nofollow. class=.external text. href=.http://gallica.bnf.fr/ark:/12148/([^\"]*).>Bibliothèque nationale de France"]
regexDict["status"] = ["Avancement</th><td><a href=.[^\"]*. title=.[^\"]*.>([^<]*)</a>"]


# == List of chosen books ==
# Possible to focus on a category using Petscan.
# Example with books from Gallica:
# https://petscan.wmflabs.org/?language=fr&project=wikisource&categories=Facsimil%C3%A9s+issus+de+Gallica&ns%5B0%5D=1&ns%5B112%5D=1&doit=1
books = [
"Abrant%C3%A8s%20-%20L%E2%80%99exil%C3%A9%20%3A%20une%20rose%20au%20d%C3%A9sert.djvu",
"Adam%20-%20Mes%20premi%C3%A8res%20armes%20litt%C3%A9raires%20et%20politiques.djvu"]


def downloadBookPages(books, urlBegin, urlEnd):
   bookNb = 0   
   for book in books:
      bookNb += 1
      print("Treating book "+str(bookNb)+"/"+str(len(books))+": "+book)

      # get webpage from Wikisource
      with urllib.request.urlopen(urlBegin+book+urlEnd) as response, open(os.path.join("webpages",book+".html"), 'wb') as out_file:
         data = response.read() # a `bytes` object
         out_file.write(data)

def getMetadata(file):
   lines = open(file,"r",encoding="utf-8").readlines()
   bookMetadata = {}
   for line in lines:
      # Look for any expected metadata on this line:
      for dataType in regexDict.keys():
         # Try all possible regex to extract this metadata:
         for regex in regexDict[dataType]:
            res = re.search(regex,line)
            #print("looking for "+dataType+" with regex "+regex)
            if res:
               bookMetadata[dataType] = res.group(1)
               #print(dataType+": "+res.group(1))
   return bookMetadata

# == First step == 
# Download the index page of a list of Wikisource books 
# in a "webpages" folder which must be located in the same folder as ws-metadata.py

downloadBookPages(books, urlBegin, urlEnd)

# == Second step ==
# Extract information from those webpages 
# and save the obtained metadata in wikisource.csv

folder = os.path.abspath(os.path.dirname(sys.argv[0]))

# List of all downloaded files:
allDownloadedFiles = glob.glob(os.path.join(folder,os.path.join("webpages","*.html")))
fileNb = len(allDownloadedFiles)

# Number of treated books so far:
bookNb = 0

# Output file
output = open("bookMetadata.csv","w",encoding="utf-8")

# Add first line with headers
for type in metadata:
   output.writelines(type+",")
output.writelines("\n")

for file in allDownloadedFiles:
   bookNb += 1
   print("Extracting metadata from file "+str(bookNb)+"/"+str(fileNb)+": "+file)
   bookMetadata = getMetadata(file)
   output.writelines('"'+file.replace('"','""')+'"')
   for type in metadata:
      if type in bookMetadata:
         output.writelines(',"'+bookMetadata[type].replace('"','""')+'"')
      else:
         output.writelines(',""')
   output.writelines("\n")

output.close()