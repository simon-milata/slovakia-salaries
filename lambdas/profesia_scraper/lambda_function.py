import json

from scraping_utils import get_side_panel_sections, get_all_salaries, get_companies
from s3_utils import save_to_s3


BASE_URL = "https://www.profesia.sk/en/work"
COMPANIES_URL = f"{BASE_URL}/list-of-companies/"


def lambda_handler(event, context) -> None:
    result_dict = get_side_panel_sections(BASE_URL)
    result_dict["salaries"] = get_all_salaries(result_dict["regions"])
    result_dict["companies"] = get_companies(COMPANIES_URL)

    result_json = json.dumps(result_dict)

    save_to_s3(result_json)


if __name__ == "__main__":
    lambda_handler(None, None)