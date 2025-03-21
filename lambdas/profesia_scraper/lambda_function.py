import os
import logging

from scraping.scraping_utils import get_html, get_list_values
from scraping.company_scraping import get_companies
from scraping.salary_scraping import get_all_salaries
from scraping.stats_scraping import get_side_panel_sections
from s3_utils import save_to_s3


# Check if running on lambda
if not "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from dotenv import load_dotenv
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    load_dotenv(env_path)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    force=True
)


BASE_URL = os.getenv("BASE_URL")
COMPANIES_URL = os.getenv("COMPANIES_URL")


def lambda_handler(event, context) -> None:
    stats_html = get_html(BASE_URL)
    stats_dict = get_side_panel_sections(stats_html)
    save_to_s3(stats_dict, "stats")

    salaries_dict = get_all_salaries(stats_dict["regions"])
    save_to_s3(salaries_dict, "salaries")

    companies_html = get_html(COMPANIES_URL)
    companies_dict = get_list_values(companies_html)
    save_to_s3(companies_dict, "companies")


if __name__ == "__main__":
    lambda_handler(None, None)