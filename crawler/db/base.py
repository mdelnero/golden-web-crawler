from crawler.webpage import WebPage
from crawler.webimage import WebImage

class PageAdapter:
    name: str

    def __init__(self):
        self.name = 'undefined'

    def get_type(self):
        return self.name
    
    def insert_page(self, page: WebPage):
        print("page none")

    def insert_image(self, img: WebImage):
        print("img none")

    def update_img(self, doc):
        print("img none")

    def read_img_to_download(self):
        print("img none")