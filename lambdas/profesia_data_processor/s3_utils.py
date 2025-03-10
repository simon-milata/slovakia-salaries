import boto3
import os
import gzip
import json
import logging
import datetime


# Check if running on lambda
if not "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from dotenv import load_dotenv
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    load_dotenv(env_path)


BUCKET = os.getenv("BUCKET")
DATA_DIRECTORY = os.getenv("DATA_DIRECTORY")


S3 = boto3.client("s3")


def load_raw_file(key: str) -> dict:
    """Loads a compress JSON file from s3, decompresses it and returns it as a dict"""
    logging.info(f"Loading {key}")
    
    s3_object = S3.get_object(Bucket=BUCKET, Key=key)
    compressed_data = s3_object["Body"].read()
    
    decompressed_data = gzip.decompress(compressed_data)
    return json.loads(decompressed_data)


def get_processed_file_path(file_name: str, date: str):
    """Returns file path based on current date."""
    file_path = f"{DATA_DIRECTORY}/{date}/{file_name}.json.gz"

    return file_path


def compress_dict(data: dict) -> bytes:
    """Converts a dict into a json, encodes it to bytes and compresses it."""
    logging.info("Compressing data.")

    data_json = json.dumps(data, ensure_ascii=False)
    data_bytes = data_json.encode("utf-8")

    return gzip.compress(data_bytes)


def save_to_s3(content: dict, file_name: str, date: str):
    content = compress_dict(content)
    file_path = get_processed_file_path(file_name, date)

    logging.info(f"Saving {file_name} data to {BUCKET}/{file_path}.")

    S3.put_object(
            Bucket=BUCKET, 
            Key=file_path, 
            Body=content,
            ContentType="application/json",
            ContentEncoding="gzip"
        )