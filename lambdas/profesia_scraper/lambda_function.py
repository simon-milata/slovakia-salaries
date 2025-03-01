from bs4 import BeautifulSoup

from scraping_utils import get_html, get_all_salaries, get_side_panel_sections


BASE_URL = "https://www.profesia.sk/praca/"


def lambda_handler(event, context) -> None:
    html = get_html(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")


if __name__ == "__main__":
    lambda_handler(None, None)