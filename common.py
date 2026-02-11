import requests
from bs4 import BeautifulSoup


def getContentFromUrl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")
