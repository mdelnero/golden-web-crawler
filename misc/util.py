from urllib.parse import urlparse
import requests
import hashlib
import re
import pymongo

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def remove_items_containing_text(lst, texts_to_remove):
    return [item for item in lst if not any(text in item for text in texts_to_remove)]

def remove_duplicates(input_list):
    unique_items = set(input_list)
    result_list = list(unique_items)
    return result_list

def get_string_hash(input_string):
    input_bytes = input_string.encode('utf-8')    
    sha256_hash = hashlib.sha256(input_bytes).hexdigest()
    return sha256_hash

class MongoAdapter:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://root:123@localhost:27017/")
        self.db = self.client["scraperPumaV3"]
        self.collection = self.db["page"]
        self.img_collection = self.db["page_img"]

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
    
    def read_all_img(self):
        query = {"content": None}
        result = self.img_collection.find(query)
        return result
    
    def read_all_failed_img(self):
        query = {"file_size": None}
        result = self.img_collection.find(query)
        return result
    
    def update_img(self, doc):
        self.img_collection.update_one(
            {'_id': doc["_id"]}, 
            {'$set': {
                'url': doc["url"],
                'short_url': doc["short_url"],
                'width': doc["width"],
                'height': doc["height"],
                'file_size': doc["file_size"],
                'content': doc["content"]
                }})