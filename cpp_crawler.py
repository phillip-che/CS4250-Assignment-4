from bs4 import BeautifulSoup
from urllib.request import urlopen
from pymongo import MongoClient
import re 

def connectDB():
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        print("Database connected successfully")
        return db
    except:
        print("Database not connected successfully")

def crawlerThread(frontier, pagesCol):
    visited = set()
    while frontier:
        url = frontier.pop()
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')

        pagesCol.insert_one({"url": url, "html": str(bs)})

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

def main():
    db = connectDB()
    pagesCol = db.pages

    frontier = ["https://www.cpp.edu/sci/computer-science/"]
    crawlerThread(frontier, pagesCol)

main()