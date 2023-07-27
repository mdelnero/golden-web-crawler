from bs4 import BeautifulSoup
from util import *



class WebPage:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.has_content = False
        self.saved = False

    def display(self):
        print(f"PAGE: {self.title} [{self.url}]")

    def fetch(self):
        if self.has_content == False:
            self.has_content = True
            self.links = set()
            self.img_links = set()
            self.content = get_http(self.url)
            soup = BeautifulSoup(self.content, "html.parser")
            self.title = soup.title.string.strip() if soup.title else None
            for link in soup.find_all("a", href=True):
                new_link = link["href"]
                if is_same_domain(new_link, self.url):
                    self.links.add(new_link)
            for link in soup.find_all('img'):
                new_link = link["src"]
                if new_link:
                    self.img_links.add(new_link)

    def save(self):
        folder = "c:\\temp\\"
        if self.has_content and not self.saved:
            self.saved = True
            with open(f"{folder}{sanitize_filename(self.url)}.html", 'w', encoding='utf-8') as f:
                f.write(f"{self.url}\n{self.title}\n\n{self.content}")

    def dispose(self):
        self.links = None
        self.img_links = None
        self.content = None