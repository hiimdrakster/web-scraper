import sys
import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup #This will probably need to be installed with 'pipX install beautifulsoup4' where X is your pip version

def scrape(web):
    print("Data scraping web... " + web)
    
    response = requests.get(web)

    #Setup the output in append mode:
    #   (each time the file is written it will jump to the end of the file and start writing from there)
    #The output path will be taken as the second argument
    output = open(sys.argv[2],"a")
    
    soup = BeautifulSoup(response.text,"html.parser")
    time.sleep(5)   #Waits 5 sec to load the page
    #Store the specified tags in an array
    tags = sys.argv[3].split(",")
    #BS will select any element with the specified tag at the third argument
    for tag in tags:
        for text in soup.findAll(tag):
            strout = re.sub(r'<.+?>','',str(text))  #Removes tags ('<p>...</p>') and it's atributes from the output text
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

        arg3: HTML tags to scrape
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
