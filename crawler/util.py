from urllib.parse import urlparse
import requests

def get_http_request(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html"
    }
    r = requests.get(url, headers)
    return r.text

def is_same_domain(link1, link2):
    domain1 = urlparse(link1).netloc
    domain2 = urlparse(link2).netloc
    return domain1.replace('www.', '') == domain2.replace('www.', '')

def transform_https_to_http(url):
    if url.startswith("https://"):
        return url.replace("https://", "http://", 1)
    else:
        return url

def remove_items_containing_text(lst, texts_to_remove):
    return [item for item in lst if not any(text in item for text in texts_to_remove)]