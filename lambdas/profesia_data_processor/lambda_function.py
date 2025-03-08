import json
import logging


from processing import process_salaries, process_stats, process_companies


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    force=True
)


def lambda_handler(event, context):
    logging.debug(event, context)

    key = event["Records"][0]["s3"]["object"]["key"]

    if key.endswith("stats.json.gz"):
        process_stats(key)
    elif key.endswith("salaries.json.gz"):
        process_salaries(key)
    elif key.endswith("companies.json.gz"):
        process_companies(key)


if __name__ == "__main__":
    event = """
    {
        "Records": [
            {
                "eventSource": "aws:s3",
                "awsRegion": "eu-central-1",
                "eventTime": "2025-03-08T10:06:07.768Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "object": {
                        "key": "raw/2025-03-08/stats.json.gz"
                    }
                }
            }
        ]
    }
    """
    lambda_handler(json.loads(event), None)