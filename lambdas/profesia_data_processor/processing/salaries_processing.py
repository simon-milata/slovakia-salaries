import re
import logging


def process_salaries(data_dict: dict) -> dict:
    pattern = r"\d+\.\d+|\d+"

    for region in data_dict:
        logging.info(f"Processing salaries for {region}.")
        processed_salaries = []

        for salary in data_dict[region]:
            processed_salary = salary.replace(",", ".")
            if "-" in salary:
                # if there is a range take the first number (minimum)
                processed_salary = processed_salary.split("-")[0]
            
            processed_salary = "".join(re.findall(pattern, processed_salary))
            if not processed_salary:
                logging.debug(f"No number in salary found. Salary: {salary}")
                continue

            processed_salary = float(processed_salary)

            if "hour" in salary:
                # convert to monthly (assuming 40h work week)
                processed_salary *= 160

            processed_salaries.append(processed_salary)

        data_dict[region] = processed_salaries
    return data_dict