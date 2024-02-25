import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from typing import Optional

from app.config import (
    AWS_DEFAULT_REGION,
    AWS_DEFAULT_ACCESS_KEY_ID,
    AWS_DEFAULT_SECRET_ACCESS_KEY,
)


def upload_file(file:Optional[UploadFile], path: str) -> bool:
    if file is None:
        return False

    # The name of the s3 bucket we want to upload to
    BUCKET_NAME = "captics-files"

    temp_file = file.file

    s3_client = boto3.client(
        "s3",
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_DEFAULT_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_DEFAULT_SECRET_ACCESS_KEY,
    )

    try:
        s3_client.upload_fileobj(temp_file, BUCKET_NAME, path)
        print("File uploaded successfully!")
        return True
    except ClientError as e:
        print("Error uploading file!")
        print(e.response["Error"]["Message"])
        return False
