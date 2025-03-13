import json
import logging

from scraping.scraping_utils import get_html
from scraping.company_scraping import get_companies
from scraping.salary_scraping import get_all_salaries
from scraping.stats_scraping import get_side_panel_sections
from s3_utils import save_to_s3


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    force=True
)


BASE_URL = "https://www.profesia.sk/en/work"
COMPANIES_URL = f"{BASE_URL}/list-of-companies/"


def lambda_handler(event, context) -> None:
    stats_dict = get_side_panel_sections(BASE_URL)
    save_to_s3(stats_dict, "stats")

    salaries_dict = get_all_salaries(stats_dict["regions"])
    save_to_s3(salaries_dict, "salaries")

    companies_html = get_html(COMPANIES_URL)
    companies_dict = get_companies(companies_html)
    save_to_s3(companies_dict, "companies")


if __name__ == "__main__":
    lambda_handler(None, None)