import os
import logging
import datetime
import gzip
import json

from dotenv import load_dotenv
import boto3


# Check if running on lambda
if not "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    load_dotenv(env_path)


BUCKET = os.getenv("BUCKET")
DATA_DIRECTORY = os.getenv("DATA_DIRECTORY")

S3 = boto3.client("s3")


def compress_dict(data: dict) -> bytes:
    """Converts a dict into a json, encodes it to bytes and compresses it."""
    logging.info("Compressing data.")

    data_json = json.dumps(data, ensure_ascii=False)
    data_bytes = data_json.encode("utf-8")

    return gzip.compress(data_bytes)


def get_raw_file_path(file_name: str):
    """Returns file path based on current date."""
    date = datetime.datetime.now().date()
    file_path = f"{DATA_DIRECTORY}/{date}/{file_name}.json.gz"

    return file_path


def save_to_s3(content: dict, file_name: str):
    content = compress_dict(content)
    file_path = get_raw_file_path(file_name)

    logging.info(f"Saving file_name data to {BUCKET}/{file_path}.")

    S3.put_object(
            Bucket=BUCKET, 
            Key=file_path, 
            Body=content,
            ContentType="application/json",
            ContentEncoding="gzip"
        )
