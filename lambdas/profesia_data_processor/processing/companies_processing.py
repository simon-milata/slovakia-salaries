import re
import logging


def process_companies(data_dict: dict) -> dict:
    data_dict = process_company_names(data_dict)

    return data_dict


def process_company_names(data_dict: dict) -> dict:
    """Removes special characters from company names and removes invalid comapnies"""
    processed_dict = {}

    logging.info("Processing company names.")

    for company, company_value in data_dict.items():

        processed_name = clean_company_name(company)

        if not processed_name:
            logging.info(f"Couldn't process company name '{company}'.")
            continue

        processed_dict[processed_name] = company_value

    return processed_dict


def clean_company_name(company_name: str) -> str | None:
    processed_name = company_name

    m = re.search(r"[a-žA-Ž0-9]", processed_name)
    if not m:
        return

    processed_name = re.sub(r"[^a-žA-Ž0-9\s,.-]", "", processed_name)
    processed_name = re.sub(r"\s+", " ", processed_name)

    return processed_name


def get_total_companies(data_fict: dict) -> int:
    pass