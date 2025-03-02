import requests
import logging

from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S,%f"
)


def get_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    return response.text


def get_soup(url: str) -> BeautifulSoup:
    html = get_html(url)

    return BeautifulSoup(html, "html.parser")
    

def get_salaries_from_page(url: str) -> list[str]:
    soup = get_soup(url)

    salaries_html = soup.find_all("span", {"class": "label label-bordered green half-margin-on-top"})

    if not salaries_html:
        logging.warning(f"No salaries scraped from {url}. Possible website change.")
        return []

    salaries = [salary.text.strip() for salary in salaries_html]
    
    logging.info(f"Scraped {len(salaries)} salaries from {url}\n")

    return salaries


def get_all_salaries(url: str) -> list[str]:
    """Returns a list of salaries from 50 pages"""
    salaries = []

    for page_number in range(1, 50 + 1):
        url = f"{url}/?page_num={page_number}"

        salaries.extend(get_salaries_from_page(url))

    return salaries


def get_dict_from_section(section) -> dict[str, str]:
    """Creates a dictionary from a side panel section"""
    section_dict = {}

    section_values = section.find_all("li")

    for value in section_values:
        if "»" in value.text:
            continue

        value_count = value.find("span").text.strip()
        value_name = value.text.replace(value_count, "").strip()

        section_dict[value_name] = value_count

    return section_dict


def get_side_panel_sections(url: str) -> dict[str, dict[str, str]]:
    """Returns a dictionary with section title as the key and a dictionary as a value"""
    sections_dict = {}

    soup = get_soup(url)

    section_filter = ["Pozícia", "Pracovná oblasť", "Ponuky spoločnosti", "Jazykové znalosti"]

    side_panel = soup.find("div", {"class": "sidebar-left"})
    sections = side_panel.find_all("section")

    if not sections:
        logging.warning(f"HTML not found for {url}. Possible website change.")
        return {}

    for section in sections:
        section_title = section.find("h3", {"class": "panel-title"}).text.strip()

        if section_title in section_filter:
            continue

        section_dict = get_dict_from_section(section)

        if not section_dict:
            logging.warning(f"No items scraped from section {section_title}.")
        else:
            logging.info(f"Scraped {len(section_dict)} items from section '{section_title}'.")

        sections_dict[section_title] = section_dict

    return sections_dict


def get_card_dict(url: str) -> dict[str, str]:
    """Returns a dictionary from a card section with value name as key and value amount as value"""
    result_dict = {}

    soup = get_soup(url)

    lists_html = soup.find("div", {"class": "card"}).find_all("li")

    if not lists_html:
        logging.warning(f"HTML not found for {url}. Possible website change.")
        return {}

    for listing in lists_html:
        listing_value = listing.find("span").text.strip()
        listing_name = listing.text.replace(listing_value, "").strip()

        result_dict[listing_name] = listing_value

    logging.info(f"Scraped {len(result_dict)} items from {url}.")

    return result_dict
