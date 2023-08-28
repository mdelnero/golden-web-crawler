from crawler.webpage import *
from crawler.webimage import *
from crawler.transformer import *
from crawler.util import *
from crawler.db.base import PageAdapter

class WebCrawler:
    url: str
    ignore_list: list[str]
    adapter: PageAdapter
    transformer: PageTransformer

    def __init__(self, 
            url: str, 
            ignore_list: list[str] = None, 
            adapter: PageAdapter = None, 
            transformer: PageTransformer = None):
        self.url = url
        self.ignore_list = ignore_list
        self.adapter = adapter
        self.transformer = transformer

    def run(self):
        root_page = WebPage(self.url)
        dic_images = dict()
        dic_pages = dict()    
        dic_pages[root_page.url] = root_page

        while True:
            initial_count = len(dic_pages)
            current_pass = set(dic_pages.values())
            for page in current_pass:
                if page.has_content == False:
                    if page.fetch():
                        page.display()
                        if self.ignore_list != None:
                            page.links = remove_items_containing_text(page.links, self.ignore_list)
                        page.img_links = list(page.img_links)
                        for item in page.links:
                            if not item in dic_pages:
                                dic_pages[item] = WebPage(item)
                        for item in page.img_links:
                            if not item in dic_images:
                                dic_images[item] = WebImage(item)
                        if self.transformer != None:
                            self.transformer.transform(page)

            for page in dic_pages.values():
                if page.has_content and not page.saved:
                    if self.adapter != None:
                        self.adapter.insert_page(page)
                    page.saved = True
                    page.dispose()

            for image in dic_images.values():
                if not image.saved:
                    if self.adapter != None:
                       self.adapter.insert_image(image)
                    image.saved = True

            final_count = len(dic_pages)
            if initial_count == final_count:
                break