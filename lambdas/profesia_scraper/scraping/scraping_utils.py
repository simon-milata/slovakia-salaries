import requests
import logging

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


def get_list_values(html: str) -> dict[str, dict[str, str]]:
    """Returns a dictionary of all listings with name as key and a dictionary with number of listings and url as value"""
    soup = BeautifulSoup(html, "html.parser")

    # try to get listing type for logging purposes e.g. "companies" except for unit tests
    try:
        listing_type = soup.find("h1").text.strip().split()[-1]
    except AttributeError:
        listing_type = "listings"

    html_elements = soup.find("ul", {"class": "list-reset"}).find_all("li")

    if not html_elements:
        logging.warning(f"No {listing_type} scraped. Possible website change?")
        return {}

    listings = parse_list_values(html_elements)

    logging.info(f"Scraped {len(listings)} {listing_type}.")

    return listings


def parse_list_values(html_elements) -> dict[str, dict[str, str]]:
    """Gets the name, numbers of listings and url for each listing"""
    listings = {}

    for company in html_elements:
        listing_count = company.find("span").text.strip()
        listing_name = company.find("a").text.strip()
        listing_url = company.find("a").get("href")

        listings[listing_name] = {"number_of_listings": listing_count, "url": listing_url}

    return listings