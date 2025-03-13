import logging

from scraping.scraping_utils import get_soup


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