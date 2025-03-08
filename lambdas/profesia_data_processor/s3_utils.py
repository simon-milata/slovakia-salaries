import boto3
import os
import gzip
import json
import logging


# Check if running on lambda
if not "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    from dotenv import load_dotenv
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    load_dotenv(env_path)


BUCKET = os.getenv("BUCKET")


def load_raw_file(key: str) -> dict:
    """Loads a compress JSON file from s3, decompresses it and returns it as a dict"""
    logging.info(f"Loading {key}")
    s3 = boto3.client("s3")
    
    s3_object = s3.get_object(Bucket=BUCKET, Key=key)
    compressed_data = s3_object["Body"].read()
    
    decompressed_data = gzip.decompress(compressed_data)
    return json.loads(decompressed_data)