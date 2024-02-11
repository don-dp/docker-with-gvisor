import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import os

def get_sanitized_content():
    url = os.getenv('url')
    if url is None:
        print("Error: url not provided.")
        return
    
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        print("Error: Invalid URL scheme")
        return
    sanitized_url = urlunparse(parsed)
    
    response = requests.get(sanitized_url, timeout=5)
    if not response.ok:
        print("Error: Unable to fetch url content.")
        return
    
    max_size=1e6
    if len(response.content) > max_size:
        print("Error: Response too large")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.get_text(separator=' ', strip=True))

if __name__ == "__main__":
    get_sanitized_content()