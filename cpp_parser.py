from bs4 import BeautifulSoup
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


def parserThread(db):
    pagesCol = db.pages
    professorsCol = db.professors
    page = pagesCol.find_one({"url":"https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"})
    bs = BeautifulSoup(page["html"], 'html.parser')

    for profDiv in bs.find_all("div", {"class":"clearfix"}):
      if profDiv.img:
        profData = {
            "name": profDiv.h2.text,
            "title": profDiv.p.find("strong", string=re.compile("Title")).next_sibling.replace(":", "").strip(),
            "office": profDiv.p.find("strong", string=re.compile("Office")).next_sibling.replace(":", "").strip(),
            "phone": profDiv.p.find("strong", string=re.compile("Phone")).next_sibling.replace(":", "").strip(),
            "email": profDiv.p.find("a", string=re.compile("@cpp.edu")).text.strip(),
            "website": profDiv.p.find("a", string=re.compile("cpp.edu/")).text.strip(),
        }
        professorsCol.insert_one(profData)

def main():
    db = connectDB()
    parserThread(db)
  
main()