from crawler.webpage import *

class PageTransformer:
    name: str

    def __init__(self):
        self.name = 'undefined'

    def get_type(self):
        return self.name
    
    def transform(self, page: WebPage):
        None