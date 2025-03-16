import logging

from bs4 import BeautifulSoup

from scraping.scraping_utils import get_html


def get_salaries_from_page(html: str) -> list[str]:
    """Scrapes all salaries from a url"""
    soup = BeautifulSoup(html, "html.parser")

    salaries_html = soup.find_all("span", {"class": "label label-bordered green half-margin-on-top"})

    salaries = [salary.text.strip() for salary in salaries_html]

    return salaries


def get_salaries_for_region(url: str) -> list[str]:
    """Returns a list of salaries for a region"""
    region_salaries = []

    for page_number in range(1, 10 + 1):
        page_url = f"{url}&page_num={page_number}"

        salaries_html = get_html(page_url)
        salaries = get_salaries_from_page(salaries_html)

        if not salaries:
            logging.warning(f"No salaries scraped from {url}. Possible website change?")
            continue
    
        region_salaries.extend(salaries)

    return region_salaries


def get_all_salaries(regions_dict: dict[str, dict[str, str]]) -> dict[str, list[str]]:
    """Returns a dictionary with region name as key and list of salaries as value"""
    if not regions_dict:
        logging.warning("Regions data are empty. Unable to get salaries. Possible webstie change?")
        return {}

    salaries = parse_salaries(regions_dict)

    return salaries


def parse_salaries(regions_dict: dict[str, dict[str, str]]) -> dict[str, list[str]]:
    salaries = {}

    for region in regions_dict:
        region_url = regions_dict[region]["url"] + "?salary=1&salary_period=m" # Modify url to only show listings with salary listed

        region_salaries = get_salaries_for_region(region_url)

        logging.info(f"Scraped {len(region_salaries)} salaries from {region_url}.")

        salaries[region] = region_salaries

    return salaries