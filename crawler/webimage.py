from crawler.util import *
import os
from urllib.parse import urlparse
import requests
import requests
import os
from PIL import Image

folder_path = "c:\\temp\\"

class WebImage:
    url: str
    short_url: str
    width: int
    height: int
    file_size: int

    def __init__(self, url):
        self.url = transform_https_to_http(url)
        self.short_url = generate_short_name(url)
        self.has_content = False
        
    def fetch(self, destination_path=""):
        try:
            path = os.path.join(folder_path, destination_path)
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