import json
import logging

from s3_utils import load_raw_file, save_to_s3
from processing.preprocessing import convert_dict_to_lowercase, convert_nested_key_to_int, rename_dict_keys
from processing.stats_processing import process_stats
from processing.salaries_processing import process_salaries
from processing.companies_processing import process_companies


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    force=True
)


def lambda_handler(event, context):
    key = event["Records"][0]["s3"]["object"]["key"]
    data_dict = load_raw_file(key)

    if key.endswith("stats.json.gz"):
        data_dict = convert_dict_to_lowercase(data_dict)
        data_dict = convert_nested_key_to_int(data_dict, "count")
        data_dict = rename_dict_keys(data_dict)
        data_dict = process_stats(data_dict)
        
    elif key.endswith("salaries.json.gz"):
        data_dict = convert_dict_to_lowercase(data_dict)
        data_dict = process_salaries(data_dict)

    elif key.endswith("companies.json.gz"):
        data_dict = convert_nested_key_to_int(data_dict, "number_of_listings")
        data_dict = process_companies(data_dict)

    file_name = key.split("/")[-1].split(".")[0]
    date = key.split("/")[1]
    save_to_s3(data_dict, file_name, date)


if __name__ == "__main__":
    event = """
    {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": "raw/2025-03-20/companies.json.gz"
                    }
                }
            }
        ]
    }
    """
    lambda_handler(json.loads(event), None)