import pymongo

from crawler.db.base import PageAdapter
from crawler.webpage import WebPage
from crawler.webimage import WebImage

class MongoPageAdapter(PageAdapter):
    def __init__(self, conn_string: str, db: str, collection: str):
        self.name = 'mongo'
        self.client = pymongo.MongoClient(conn_string)
        self.db = self.client[db]
        self.page_collection = self.db[collection]
        self.img_collection = self.db[collection + '_img']

    def insert_page(self, page: WebPage):
        data = {
            "url": page.url,
            "title": page.title,
            "content": page.content,
            "plain_text": page.plain_text,
            "tags": page.tags,
            "links": page.links,
            "img_links": page.img_links,
            "elected": page.elected}
        
        result = self.page_collection.insert_one(data)
        print("- PAGE ID:", result.inserted_id)

    def insert_image(self, img: WebImage):
        data = {
            "url": img.url,
            "short_url": img.short_url,
            "content": None}
        result = self.img_collection.insert_one(data)
        print("- IMG ID:", result.inserted_id)

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

    def read_img_to_download(self):
        query = {"content": None}
        result = self.img_collection.find(query)
        return result