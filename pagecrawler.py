from crawler import WebCrawler
from crawler.db import MongoPageAdapter
from plain_text_transformer import *

# "http://fuscaclassic.blogspot.com/2009/03/hebmuller.html"

def main() -> None:

    db = MongoPageAdapter("mongodb://root:123@localhost:27017/", "scraperPuma", "page")
    transformer = PlainTextTransformer()

    crawler = WebCrawler(
        url= "http://www.pumaclassic.com.br/index.html" ,
        ignore_list=["#main", "#sidebar", "feeds/", "search/label/", "search?", "?showComment=", "javascript:void(0)"], 
        adapter=db,
        transformer=transformer)
    
    crawler.run()

if __name__ == '__main__':
    main()