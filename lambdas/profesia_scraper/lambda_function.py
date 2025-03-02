from bs4 import BeautifulSoup

from scraping_utils import get_card_dict


BASE_URL = "https://www.profesia.sk/praca"
DISTRICTS_URL = f"{BASE_URL}/zoznam-lokalit"
POSITIONS_URL = f"{BASE_URL}/zoznam-pozicii"
INDUSTRY_URL = f"{BASE_URL}/zoznam-pracovnych-oblasti"
LANGUAGES_URL = f"{BASE_URL}/zoznam-jazykovych-znalosti"


def lambda_handler(event, context) -> None:
    pass


if __name__ == "__main__":
    lambda_handler(None, None)