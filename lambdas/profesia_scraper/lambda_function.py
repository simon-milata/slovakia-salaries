from bs4 import BeautifulSoup

from scraping_utils import get_side_panel_sections


BASE_URL = "https://www.profesia.sk/en/work/"
DISTRICTS_URL = f"{BASE_URL}/list-of-location"
POSITIONS_URL = f"{BASE_URL}/list-of-positions"
INDUSTRY_URL = f"{BASE_URL}/list-of-work-areas"
LANGUAGES_URL = f"{BASE_URL}/list-of-language-skills"


def lambda_handler(event, context) -> None:
    pass


if __name__ == "__main__":
    lambda_handler(None, None)