#   By: Sasan Najar
#   Email: sasangnajar@gmail.com

#   This code is to:
##  STEP1: Go to a random Wikipedia page and click the fisrt link
##  STEP2:  Then on that page click the first link in the main body of the article text

import requests
import time
import urllib
import bs4

startURL = "https://en.wikipedia.org/wiki/Special:Random"
targetURL = "https://en.wikipedia.org/wiki/Philasophy"

def getFirstLink(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')     # make soup obj of html
    contentdiv = soup.find(id='mw-content-text').find(class_="mw-parser-output") #first link
    #if the article contains no links this value will remain None
    articleLink = None
    # find all the direct children of contentdiv that are paragraghs
    for element in contentdiv.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            articleLink = element.find("a", recursive=False).get('href')
            break
    if not articleLink:
        return
    # Build a full url from the relative articleLink url
    firstLink = urllib.parse.urljoin('https://en.wikipedia.org/', articleLink)
    return firstLink

#countinueCrawl function
#continueCrawl should return True or False following these rules:
#if the most recent article in the searchHistory is the target article the search should stop and the function should return False
#If the list is more than 25 urls long, the function should return False
#If the list has a cycle in it, the function should return False
#otherwise the search should continue and the function should return True.

def countinueCrawl(searchHistory, targetURL, maxSteps=25):
    if searchHistory[-1] == targetURL:
        print("target article found")
        return False
    elif len(searchHistory) > maxSteps:
        print("search too long -- aborting search ...")
        return False
    elif searchHistory[-1] in searchHistory[:-1]:
        print("repeated article -- aborting search ...")
        return False
    else:
        return True

articleChain = [startURL]

while countinueCrawl(articleChain, targetURL):
    #print(articleChain[-1])
    firstLink = getFirstLink(articleChain[-1])
    if not firstLink:
        print("article with no links -- aborting search")
        break
    articleChain.append(firstLink)
    time.sleep(2)
