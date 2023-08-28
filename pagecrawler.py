from crawler import WebCrawler, ImageCrawler
from crawler.db import MongoPageAdapter
from plain_text_transformer import *

# "http://fuscaclassic.blogspot.com/2009/03/hebmuller.html"

def main() -> None:

    db = MongoPageAdapter("mongodb://root:123@localhost:27017/", "scraperPumaV3", "page")
    transformer = PlainTextTransformer()

    crawler = WebCrawler(
        url= "http://www.pumaclassic.com.br/index.html",
        #url= "http://fuscaclassic.blogspot.com/index.html",
        ignore_list=["#main", "#sidebar", "feeds/", "search/label/", "search?", "?showComment=", "javascript:void(0)"], 
        adapter=db,
        transformer=transformer)
    
    # crawler.run()

    img_crawler = ImageCrawler(
        download_path="c:\\temp\\xpto",
        adapter=db)
    
    img_crawler.run()

if __name__ == '__main__':
    main()