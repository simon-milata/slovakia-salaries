import requests
import logging

from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)


def get_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    return response.text
    

def get_salaries_from_page(url: str) -> list[str]:
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    salaries_html = soup.find_all("span", {"class": "label label-bordered green half-margin-on-top"})

    salaries = [salary.text.strip() for salary in salaries_html]
    
    logging.info(f"Scraped {len(salaries)} salaries from {url}\n")

    return salaries


def get_all_salaries(base_url: str) -> list[str]:
    salaries = []

    for page_number in range(1, 50 + 1):
        url = f"{base_url}?page_num={page_number}"

        logging.info(f"Scraping salaries from {url}")

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


def get_side_panel_sections(soup: BeautifulSoup) -> dict[str, dict[str, str]]:
    """Returns a dictionary with section title as the key and a dictionary as a value"""
    sections_dict = {}

    section_filter = ["Pozícia", "Pracovná oblasť", "Ponuky spoločnosti", "Jazykové znalosti"]

    side_panel = soup.find("div", {"class": "sidebar-left"})
    sections = side_panel.find_all("section")

    for section in sections:
        section_title = section.find("h3", {"class": "panel-title"}).text.strip()

        if section_title in section_filter:
            continue

        section_dict = get_dict_from_section(section)

        sections_dict[section_title] = section_dict

    return sections_dict
