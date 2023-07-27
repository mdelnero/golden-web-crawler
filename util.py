from urllib.parse import urlparse
import requests
import hashlib
import re
import pymongo

def get_http(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html"
    }
    r = requests.get(url, headers)
    return r.text

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def remove_items_containing_text(lst, texts_to_remove):
    return [item for item in lst if not any(text in item for text in texts_to_remove)]

def remove_duplicates(input_list):
    unique_items = set(input_list)
    result_list = list(unique_items)
    return result_list

def is_same_domain(link1, link2):
    domain1 = urlparse(link1).netloc
    domain2 = urlparse(link2).netloc
    return domain1.replace('www.', '') == domain2.replace('www.', '')

def get_string_hash(input_string):
    input_bytes = input_string.encode('utf-8')    
    sha256_hash = hashlib.sha256(input_bytes).hexdigest()
    return sha256_hash

class MongoAdapter:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://root:123@localhost:27017/")
        self.db = self.client["scraper"]
        self.collection = self.db["pages"]

    def insert(self, page):
        data = {
            "url": page.url,
            "title": page.title,
            "content": page.content,
            "links": page.links,
            "img_links": page.img_links}
        
        result = self.collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

    def update(self, doc):
        self.collection.update_one(
            {'_id': doc["_id"]}, 
            {'$set': {'plain_text': doc["plain_text"], 'tags': doc["tags"]}})
        
    def read_query(self, query):       
        result = self.collection.find(query)
        return result

    def read_all(self):
        query = {"leaf": True}
        result = self.collection.find(query)
        return result

