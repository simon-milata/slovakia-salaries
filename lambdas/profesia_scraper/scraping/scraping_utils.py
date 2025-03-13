import requests

from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
               "Referer": "https://www.profesia.sk/"}

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    return response.text


def get_soup(url: str) -> BeautifulSoup:
    html = get_html(url)

    return BeautifulSoup(html, "html.parser")

