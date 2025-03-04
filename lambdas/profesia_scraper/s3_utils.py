import os
import logging
import datetime

from dotenv import load_dotenv
import boto3


# Check if running on lambda
if not "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, ".env")
    load_dotenv(env_path)


BUCKET = os.getenv("BUCKET")

S3 = boto3.client("s3")


def get_raw_file_path():
    date = datetime.datetime.now().date()
    file_path = f"raw/{date}/data.json"

    return file_path


def save_to_s3(content):
    file_path = get_raw_file_path()

    logging.info(f"Uploading to {BUCKET}/{file_path}")

    S3.put_object(
            Bucket=BUCKET, 
            Key=file_path, 
            Body=content,
            ContentType="application/json"
        )
