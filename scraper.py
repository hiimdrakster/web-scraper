'''
I need someone to build a Program (or script) that copies TEXT from a million websites and saves them to a text document (txt). 
The program can be built as a Python script or an Executable (or suggest an alternative).

This is how it should work:
1 > Upload website(s) into the Program
2 > Run the Program
3 > Program will go to 100 websites, and then copies the text from each one, and paste them into a text document (.txt)
4 > Program will then save the text document for those 100 websites
5 > Program will repeat steps 3, 4 and 5 for the next 100 websites

The Program Requirements:
1) The Program must be "simple" to use
2) The Program must allow me to enter unlimited number of websites quickly (bulk upload)
3) The Program must NEVER miss a website (so if the website is lagging or freezes,
then the program must wait for the page to load. If the website doesn't load after a while,
then it needs to attempt to reload the page.
4) The Program must have a LOG FILE that shows which websites have been completed,
so I can continue the Program where it left off.
'''

import sys
import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup #This will probably need to be installed with 'pipX install beautifulsoup4' where X is your pip version

def scrape(web):
    print("Data scraping web... " + web+"\n")
    
    url = web
    response = requests.get(url)

    #Setup the output in append mode:
    #   (each time the file is written it will jump to the end of the file and start writing from there)
    #The output path will be taken as the second argument
    output = open(sys.argv[2],"a")
    
    soup = BeautifulSoup(response.text,"html.parser")
    time.sleep(5)   #Waits 5 sec to load the page
    #BS will select any element with the specified tag at the third argument
    for text in soup.findAll(sys.argv[3]):
        strout = re.sub(r'<.+?>','',str(text))  #Removes tags ('<p>...</p>') and it's atributes
        output.write(strout)

def splitfile(file):
    #First read the file and store all data into a string
    strfile = file.read()
    #The function returns an array of the string separating the links using the comma as a trigger
    return strfile.split(",")

def main():
    #The program takes as a first argument the path of a .csv file as an input with the list of webs
    with open(sys.argv[1],"r") as csvfile:
        #The file is sorted into an array having each link separated
        weblist = splitfile(csvfile)
        #For each link we call the function to begin data scraping
        for web in weblist:
            scrape(web)

usage = '''- Invalid arguments -
    Usage: 
        arg1: Path of the .csv input file containing link
            (Format must be: http://example.com
                             https://example.com)
        arg2: Path for the .txt output file

        arg3: HTML tag to scrape
    '''
#Script begins
try:
    main()
except IndexError:
    print(usage)
except FileNotFoundError:
    print('''- Invalid file -
You provided an invalid path/file
    ''')
except requests.exceptions.ConnectionError:
    print('''- Invalid URL -
You provided an invalid URL
    ''')