from crawler.util import *

class WebImage:
    def __init__(self, url):
        self.url = transform_https_to_http(url)
        self.has_content = False
        self.saved = False