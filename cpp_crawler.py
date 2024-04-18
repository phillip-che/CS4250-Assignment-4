from bs4 import BeautifulSoup
from urllib.request import urlopen
import re 
import pymongo

def crawlerThread(frontier):
    visited = set()
    while frontier:
        url = frontier.pop()
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')

        # store page in mongo

        visited.add(url)

        if bs.h1.text == "Permanent Faculty":
            print("FOUND")
            frontier.clear()
        else:
            for a in bs.find_all('a', {'class':re.compile("link")}, href = True):
                link = a.get('href')
                if "https://www" not in link:
                        link = "https://www.cpp.edu" + link
                if re.search('html', link) and link not in visited:
                    frontier.append(link)

frontier = ["https://www.cpp.edu/sci/computer-science/"]
crawlerThread(frontier)