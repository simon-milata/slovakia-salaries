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
    

def get_salaries_from_page(url: str) -> list[str]:
    """Scrapes all salaries from a url"""
    soup = get_soup(url)

    salaries_html = soup.find_all("span", {"class": "label label-bordered green half-margin-on-top"})

    if not salaries_html:
        logging.warning(f"No salaries scraped from {url}. Possible website change?")
        return []

    salaries = [salary.text.strip() for salary in salaries_html]

    return salaries


def get_salaries_from_pages(url: str) -> list[str]:
    """Returns a list of salaries from 50 pages"""
    salaries = []

    for page_number in range(1, 50 + 1):
        page_url = f"{url}&page_num={page_number}"

        salaries.extend(get_salaries_from_page(page_url))

    return salaries


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

        region_salaries = get_salaries_from_pages(region_url)

        logging.info(f"Scraped {len(region_salaries)} salaries from {region_url}.")

        salaries[region] = region_salaries

    return salaries


def get_dict_from_section(base_url: str, section: str) -> dict[str, dict[str, str]]:
    """Returns a dictionary {"region_name": {"count": count, "url": url}} from a section"""
    section_elements = section.find_all("li")

    if not section_elements:
        logging.warning("Sections not found. Possible website change?")

    section_dict = parse_section(section_elements, base_url)

    return section_dict


def parse_section(section_elements, base_url: str) -> dict:
    section_dict = {}

    for element in section_elements:
        if "»" in element.text:
            continue

        value_count = element.find("span").text.strip()
        value_name = element.text.removesuffix(value_count).strip()
        value_url = f"{base_url}{element.find("a").get("href")}"

        section_dict[value_name] = {"count": value_count, "url": value_url}

    return section_dict


def get_side_panel_sections(base_url: str) -> dict[str, dict[str, str]]:
    """Returns a dictionary with section title as the key and a dictionary as a value"""
    sections_dict = {}

    soup = get_soup(base_url)

    section_filter = ["position", "working area", "jobs from the company", "language skills"]

    side_panel = soup.find("div", {"class": "sidebar-left"})
    sections = side_panel.find_all("section")

    if not sections:
        logging.warning(f"HTML not found for {base_url}. Possible website change?")
        return {}

    for section in sections:
        section_title = section.find("h3", {"class": "panel-title"}).text.strip().lower()

        if section_title in section_filter:
            continue

        section_dict = get_dict_from_section(base_url, section)

        if not section_dict:
            logging.warning(f"No items scraped from section {section_title}.")
        else:
            logging.info(f"Scraped {len(section_dict)} items from '{section_title}' section.")

        sections_dict[section_title] = section_dict

    return sections_dict


def get_card_dict(url: str) -> dict[str, str]:
    """Returns a dictionary from a card section with value name as key and value amount as value"""
    result_dict = {}

    soup = get_soup(url)

    lists_html = soup.find("div", {"class": "card"}).find_all("li")

    if not lists_html:
        logging.warning(f"HTML not found for {url}. Possible website change?")
        return {}

    for listing in lists_html:
        listing_value = listing.find("span").text.strip()
        listing_name = listing.text.removesuffix(listing_value).strip()

        result_dict[listing_name] = listing_value

    logging.info(f"Scraped {len(result_dict)} items from {url}.")

    return result_dict


def get_companies(url: str) -> dict[str, dict[str, str]]:
    """Returns a dictionary of all companies with company name as key and a dictionary with number of listings and url as value"""
    soup = get_soup(url)

    companies_html = soup.find("ul", {"class": "list-reset"}).find_all("li")

    if not companies_html:
        logging.warning(f"No companies scraped from {url}. Possible website change?")
        return {}

    companies = parse_companies(companies_html)

    logging.info(f"Scraped {len(companies)} companies from {url}.")

    return companies


def parse_companies(companies_html) -> dict:
    companies = {}

    for company in companies_html:
        company_listings_count = company.find("span").text.strip()
        company_name = company.text.strip().removesuffix(company_listings_count).strip()
        company_url = company.find("a").get("href")

        companies[company_name] = {"number_of_listings": company_listings_count, "url": company_url}

    return companies