from bs4 import BeautifulSoup
from util import *
import os
from urllib.parse import urlparse
import requests
import hashlib
import re
import pymongo
from urllib.parse import urlparse
import requests
import hashlib
import base64
import os
from PIL import Image
import shutil

root_path = "c:\\temp\\images\\"
cache_path = "c:\\temp\\images_cache\\"

db = MongoAdapter()

def generate_short_name(url, extension=True):    
    sha256_hash = hashlib.sha256(url.encode()).digest()    
    short_name = base64.urlsafe_b64encode(sha256_hash).decode().rstrip("=")
    if extension:
        file_extension = os.path.splitext(url)[1]
        short_name += file_extension
    return short_name

    
def is_html_file(file_path):
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            return first_line.startswith("<!DOCTYPE html>") or first_line.startswith("<html")
    except (IOError, UnicodeDecodeError):
        return False
    
def transform_https_to_http(url):
    if url.startswith("https://"):
        return url.replace("https://", "http://", 1)
    else:
        if url.startswith("//"):
            return "http:" + url
        else:
            return url
    
def fetch_and_img(file_path):
    img_links = set()
    with open(file_path, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all('img'):
            new_link = transform_https_to_http(link["src"])
            if new_link:
                img_links.add(new_link)
    return img_links                
    
class WebImage:
    url: str
    short_url: str
    width: int
    height: int
    file_size: int

    def __init__(self, url):
        self.url = url
        self.short_url = generate_short_name(url)
        self.has_content = False
        self.saved = False

    def fetch(self, destination_path):
        try:
            path = os.path.join(root_path, destination_path)
            if not os.path.exists(path):
                os.makedirs(path)
            if self.has_content == False:
                filename = os.path.join(path, self.short_url)         
                response = requests.get(self.url, stream=True)                
                response.raise_for_status()                
                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                self.width, self.height, self.file_size = self.get_image_details(filename)
                self.has_content = self.file_size != 0
            return self.has_content
        except Exception as e:
            print(f"An error occurred: {e}")
            self.has_content = False
            return False

    def get_image_details(self, image_path):
        try:
            with Image.open(image_path) as img:
                width, height = img.size
            file_size = os.path.getsize(image_path)
            return width, height, file_size
        except Exception as e:
            return None, None, None

def read_all_documents():
    try:        
        count = 0
        
        all_imgs = db.read_all_img()

        for doc in all_imgs:

            ix = WebImage(doc["url"])
            
            if ix.fetch(""):

                doc["short_url"] = ix.short_url
                doc["width"] = ix.width
                doc["height"] = ix.height
                doc["file_size"] = ix.file_size
                doc["content"] = ix.has_content
                db.update_img(doc)

            count = count +1
            print(count, ' - ', ix.url)

    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Make sure MongoDB is running.")

def read_all_failed_documents():
    try:        
        count = 0        
        all_imgs = db.read_all_failed_img()

        for doc in all_imgs:            
            filename_cache = os.path.join(cache_path, doc["short_url"])

            if os.path.exists(filename_cache) and is_html_file(filename_cache):
                count = count +1
                print(count, ' - ', doc["short_url"])

                links = fetch_and_img(filename_cache)

                for intem in links:
                    ix = WebImage(intem)

                    if ix.fetch(""):
                        doc["short_url"] = ix.short_url
                        doc["width"] = ix.width
                        doc["height"] = ix.height
                        doc["file_size"] = ix.file_size
                        doc["content"] = ix.has_content
                        db.update_img(doc)


    except pymongo.errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Make sure MongoDB is running.")

if __name__ == "__main__":
    read_all_failed_documents()