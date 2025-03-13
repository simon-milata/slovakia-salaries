import logging

from bs4 import BeautifulSoup


def get_companies(html: str) -> dict[str, dict[str, str]]:
    """Returns a dictionary of all companies with company name as key and a dictionary with number of listings and url as value"""
    soup = BeautifulSoup(html, "html.parser")

    companies_html = soup.find("ul", {"class": "list-reset"}).find_all("li")

    if not companies_html:
        logging.warning(f"No companies scraped. Possible website change?")
        return {}

    companies = parse_companies(companies_html)

    logging.info(f"Scraped {len(companies)} companies.")

    return companies


def parse_companies(companies_html) -> dict:
    companies = {}

    for company in companies_html:
        company_listings_count = company.find("span").text.strip()
        company_name = company.find("a").text.strip()
        company_url = company.find("a").get("href")

        companies[company_name] = {"number_of_listings": company_listings_count, "url": company_url}

    return companies