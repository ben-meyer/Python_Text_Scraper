#! python 3
# import modules
import re, os, pyperclip, requests, bs4, html2text
from bs4 import BeautifulSoup

# This file uses the html2text module to iterate through a sitemap and extract all the text on every webpage.
# To use this file, first, copy all the URLs you wish to convert to .txt file to your clipboard.
# They must be in a clean format i.e. beginning with http:// or https:// and ending with / or white space

# os.mkdir('Website_text')

# Create a Regular Expression for a web address
webAddress = re.compile(r'http://www.*|https://www.*')

# Get the text from the clipboard
text = pyperclip.paste()

# Extract the website from the text
ExtractedWebAddress = webAddress.findall(text)

# Create a blank list to store the urls
NewUrls = []

# Clean up the url strings and store them in the list
for i in ExtractedWebAddress:
	raw = re.compile('\r')
	if i.endswith('\r'):
		NewUrls.append(i.replace('\r',''))

# Create a blank dictionary to store page titles and text		
webPageText_and_title = {}

# Go through the clean urls in the NewUrls list
# Convert the webpage to text using html2text module
# Extract the title of the webpage with BeautifulSoup
# Store the title of the webpage as a key and the text as a value in the new dictionary
for cleanUrl in NewUrls:
    try:
        print('Getting: ' + cleanUrl)
        # get the clean html text
        html = requests.get(cleanUrl)
        requestText = html.text
        webPageText = html2text.html2text(requestText)
        # get the page title using Beautiful Soup
        soup = BeautifulSoup(html.text, 'html.parser')
        # strip the title tags off the string
        pageTitleTag = soup.find('title')
        pageTitle = str(pageTitleTag)
        pageTitle = pageTitle.lstrip('<title>')
        pageTitle = pageTitle.rstrip('</title>')
        # remove special characters
        pageTitle = re.sub(r'\W+', ' ', pageTitle)
        # store in the dictionary
        webPageText_and_title[pageTitle] = webPageText
    except:
        print('Received an error. Could not access ' + cleanUrl) 

# Iterate through the keys and values in the dictionary and write the files
for title, text in webPageText_and_title.items():
        try:
                file = open(str(title) + '.txt', "w")
                file.write(str(text))
                print('Writing: ' + str(title))
                file.close()
        except:
                print('Could not write file.')
        
print('Program complete!')

# Additional nice-to-have's:
# 1. Create a new folder to store the files in
# 2. Add in the urls to the .txt file so you know which webpage it was
# 3. Create the sitemap from scratch from one base_url inputted by the user
