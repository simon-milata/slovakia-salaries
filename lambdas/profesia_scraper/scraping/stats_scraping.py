import logging
import os

from bs4 import BeautifulSoup


# Check if running on lambda
if not "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from dotenv import load_dotenv
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, "..", ".env")  # .. to navigate one level up
    env_path = os.path.abspath(env_path)
    load_dotenv(env_path)


BASE_URL = os.getenv("BASE_URL")


def get_dict_from_section(section) -> dict[str, dict[str, str]]:
    """Returns a dictionary {"region_name": {"count": count, "url": url}} from a section"""
    section_elements = section.find_all("li")

    if not section_elements:
        logging.warning("Sections not found. Possible website change?")

    section_dict = parse_section(section_elements)

    return section_dict


def parse_section(section_elements) -> dict:
    section_dict = {}

    for element in section_elements:
        if "»" in element.text:
            continue

        value_count = element.find("span").text.strip()
        value_name = element.text.strip().removesuffix(value_count).strip()
        value_url = f"{BASE_URL}{element.find("a").get("href")}"

        section_dict[value_name] = {"count": value_count, "url": value_url}

    return section_dict


def get_side_panel_sections(html: str) -> dict[str, dict[str, str]]:
    """Returns a dictionary with section title as the key and a dictionary as a value for sections in the side panel"""
    sections_dict = {}

    section_filter = ["position", "working area", "jobs from the company", "language skills"]

    soup = BeautifulSoup(html, "html.parser")

    side_panel = soup.find("div", {"class": "sidebar-left"})
    sections = side_panel.find_all("section")

    if not sections:
        logging.warning(f"HTML not found for {BASE_URL}. Possible website change?")
        return {}

    for section in sections:
        section_title = section.find("h3", {"class": "panel-title"}).text.strip().lower()

        if section_title in section_filter:
            continue

        section_dict = get_dict_from_section(section)

        if not section_dict:
            logging.warning(f"No items scraped from section {section_title}.")
        else:
            logging.info(f"Scraped {len(section_dict)} items from '{section_title}' section.")

        sections_dict[section_title] = section_dict

    return sections_dict
