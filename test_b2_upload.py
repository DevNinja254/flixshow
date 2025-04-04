import boto3
from botocore.client import Config

# Configure B2 client
s3 = boto3.client(
    's3',
    aws_access_key_id='005eb8941d06f150000000001',  # Replace with your Application Key ID
    aws_secret_access_key='K005EYqUQjrbn+hnMhGPr7CUG1QghWc',  # Replace with your Application Key
    endpoint_url='https://s3.us-east-005.backblazeb2.com',  # Your bucket’s endpoint
    config=Config(signature_version='s3v4')
)

# Upload test.txt
try:
    s3.upload_file(
        'test.txt',
        'flixshow',  # Replace 'flixshow' with your bucket name
        'test.txt',
        ExtraArgs={'ChecksumAlgorithm': None}  # Disable checksum (optional, may not be needed)
    )
    print("Successfully uploaded test.txt to Backblaze B2!")
except Exception as e:
    print(f"Error uploading file: {e}")