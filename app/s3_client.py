import os
import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
S3_BUCKET = os.getenv(" E")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)
