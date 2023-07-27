from webpage import *
from util import *

db = MongoAdapter()

def run(root_page):
    ignore_list =  ["#main", "#sidebar", "feeds/", "search/label/", "search?", "?showComment=", "javascript:void(0)"]

    dic_pages = dict()    
    dic_pages[root_page.url] = root_page
    set_images = set()

    while True:
        initial_count = len(dic_pages)
        current_pass = set(dic_pages.values())
        for page in current_pass:
            if page.has_content == False:
                page.fetch()
                page.display()
                page.links = remove_items_containing_text(page.links, ignore_list)
                page.img_links = list(page.img_links)
                for item in page.links:
                    if not item in dic_pages:
                        dic_pages[item] = WebPage(item)
                for item in page.img_links:
                    set_images.add(item)  

        for page in dic_pages.values():

            if page.has_content and not page.saved:
                page.save()
                # db.insert(page)
                page.saved = True
                page.dispose()

        final_count = len(dic_pages)
        if initial_count == final_count:
            break

run( WebPage('https://www.pumaclassic.com.br/index.html') )