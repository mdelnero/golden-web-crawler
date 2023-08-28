from crawler.webimage import *
from crawler.util import *
from crawler.db.base import PageAdapter

class ImageCrawler:
    def __init__(self, 
            download_path: str,
            adapter: PageAdapter = None):
        self.download_path = download_path
        self.adapter = adapter

    def run(self):
        try:        
            count = 0            
            all_imgs = self.adapter.read_img_to_download()

            for doc in all_imgs:
                img = WebImage(doc["url"])
                
                if img.fetch():
                    doc["short_url"] = img.short_url
                    doc["width"] = img.width
                    doc["height"] = img.height
                    doc["file_size"] = img.file_size
                    doc["content"] = img.has_content
                    self.adapter.update_img(doc)

                count = count +1
                print(count, ' - ', img.url)

        except Exception as e:
            print(f"An error occurred: {e}")