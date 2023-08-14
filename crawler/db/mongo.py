import pymongo

from crawler.db.base import PageAdapter
from crawler.webpage import WebPage
from crawler.webimage import WebImage

class MongoPageAdapter(PageAdapter):
    def __init__(self, conn_string: str, db: str, collection: str):
        self.name = 'mongo'
        self.client = pymongo.MongoClient(conn_string)
        self.db = self.client[db]
        self.collection = self.db[collection]

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
        
        result = self.collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

    def insert_image(self, img: WebImage):
        data = {
            "url": img.url,
            "content": None}
