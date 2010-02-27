# admiral

admiral is a simple python webserver serving an inverted index for
for a specified folder of textfiles.

Originally it was written for the exercises of the search engine class
winter semester 09/10 at the University of Freiburg.

## Startup:
The webserver is started via the commandline in the form of:
./admiral.py -p PORT -f FOLDER -d DOCROOT
where PORT is the port the webserver should be ran at and FOLDER is the folder
with the documents to index for the search page. DOCROOT should contain html,
css, etc.

