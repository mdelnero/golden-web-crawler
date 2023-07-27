from webpage import *
from util import *
from bs4 import BeautifulSoup
from util import *
from util_text import *
import re

db = MongoAdapter()

def save(name, text):
        folder = "c:\\temp\\"
        with open(f"{folder}{name}", 'w') as f:
            f.write(text)

def read_all_documents():
    try:        
        count = 0
        
        all_documents = db.read_all() # db.read_query({"title": "Puma Classic: Puma GTE 1975 (2) - A restauração"})

        for doc in all_documents:
            soup = BeautifulSoup(doc["content"], "html.parser")

            # gets post body
            target_div = soup.find('div', {'class': 'post-body entry-content'})
            # convert <br> to LF
            for br in target_div.find_all("br"):
                br.replace_with("\n")
            # prepare
            doc['plain_text'] = prepare_text(target_div.text)

            # gets post tags
            target_label = soup.find('span', {'class': 'post-labels'})
            # split tags
            target_label = target_label.text.replace('\n', '').replace('Marcadores:', '')
            if target_label == '':
                 doc['tags'] = None
            else:
                 doc['tags'] = target_label.split(',')

            db.update(doc)

            #title=doc["title"]
            #text=doc["plain_text"]
            #save(f"{get_string_hash(title)}.txt", str(text))
            
            count = count +1
            print(count, ' - ', doc["title"])

    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Make sure MongoDB is running.")

if __name__ == "__main__":
    read_all_documents()