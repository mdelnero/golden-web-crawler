from crawler import WebCrawler
from crawler.db import MongoPageAdapter
from plain_text_transformer import *

def main() -> None:
    db = MongoPageAdapter("mongodb://root:123@localhost:27017/", "scraperXXXXyyy", "teste")
    transformer = PlainTextTransformer()

    url = "https://www.pumaclassic.com.br/index.html"
    ignore_list =  ["#main", "#sidebar", "feeds/", "search/label/", "search?", "?showComment=", "javascript:void(0)"]

    crawler = WebCrawler(url=url, ignore_list=ignore_list, adapter=db, transformer=transformer)
    crawler.run()

if __name__ == '__main__':
    main()