from bs4 import BeautifulSoup
from util_text import *
from crawler import *

class PlainTextTransformer(PageTransformer):
    def __init__(self):
        self.name = 'plain_text'

    def transform(self, page: WebPage):
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            # gets post body
            target_div = soup.find('div', {'class': 'post-body entry-content'})
            if target_div:
                # convert <br> to LF
                for br in target_div.find_all("br"):
                    br.replace_with("\n")
                # prepare
                page.plain_text = prepare_text(target_div.text)
            else:
                page.plain_text = None
        except Exception as e:
            print(f"Error processing post body: {e}")
            page.plain_text = None
        try:
            # gets post tags
            target_label = soup.find('span', {'class': 'post-labels'})
            if target_label:
                # split tags
                target_label = target_label.text.replace('\n', '').replace('Marcadores:', '')
                if target_label == '':
                    page.tags = None
                else:
                    page.tags = target_label.split(',')
            else:
                page.tags = None
        except Exception as e:
            print(f"Error processing post tags: {e}")
            page.tags = None