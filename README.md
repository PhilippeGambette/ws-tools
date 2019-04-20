# ws-metadata
Download metadata about books from Wikisource.

Please use Python3 to execute this script.

2 steps:
* Download the index page of a list of Wikisource books in a "webpages" folder which must be located in the same folder as ws-metadata.py
* Extract information from those webpages and save the obtained metadata in wikisource.csv

Please replace variable `books` on line 37 by a list of all Wikisource files you want to get metadata about. For example, you may use Petscan to download a list of books according to some criterion, like the list of all books from Gallica: https://petscan.wmflabs.org/?language=fr&project=wikisource&categories=Facsimil%C3%A9s+issus+de+Gallica&ns%5B0%5D=1&ns%5B112%5D=1&doit=1

If there is a problem with special characters, please encode the special characters in Wikisource file names, using for example urlencoder.org