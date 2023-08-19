from bs4 import BeautifulSoup
from crawler.util import *

class WebPage:
    url: str
    title: str
    content: str
    plain_text: str
    tags: list[str]
    links: set()
    img_links: set()
    elected: bool

    def __init__(self, url):
        self.url = transform_https_to_http(url)
        self.title = ""
        self.elected = False
        self.has_content = False
        self.saved = False

    def display(self):
        print(f"PAGE: {self.title} [{self.url}]")

    def fetch(self):
        try:
            if self.has_content == False:
                self.has_content = True
                self.links = set()
                self.img_links = set()

                self.content = get_http_request(self.url)
                soup = BeautifulSoup(self.content, "html.parser")
                self.title = soup.title.string.strip() if soup.title else None

                for link in soup.find_all("a", href=True):
                    new_link = transform_https_to_http(link["href"])
                    if is_same_domain(new_link, self.url):
                        self.links.add(new_link)
                    if is_image_url(new_link):
                        self.img_links.add(new_link)
                for link in soup.find_all('img'):
                    new_link = transform_https_to_http(link["src"])
                    if new_link:
                        self.img_links.add(new_link)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            self.has_content = False
            self.dispose()
            return False

    def dispose(self):
        self.links = None
        self.img_links = None
        self.content = None

        '''
    def save(self):
        folder = "c:\\temp\\"
        if self.has_content and not self.saved:
            self.saved = True
            with open(f"{folder}{sanitize_filename(self.url)}.html", 'w', encoding='utf-8') as f:
                f.write(f"{self.url}\n{self.title}\n\n{self.content}")
    '''