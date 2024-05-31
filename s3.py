import os  
import boto3  
from botocore import UNSIGNED  
from botocore.client import Config

# Configure S3 client to use unsigned requests  
s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

bucket_name = 'cse-cic-ids2018'  
prefix = ''  # Adjust the prefix if needed

# Function to list objects in the S3 bucket  
def list_objects(bucket, prefix=''):
    print(f"Listing objects in bucket: {bucket} with prefix: {prefix}")  
    objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)  
    return objects.get('Contents', [])

# Function to download an object  
def download_object(bucket, key, download_dir):
    print(f"Processing {key}")  
    if not os.path.exists(download_dir):  
        os.makedirs(download_dir)  
        print(f"Created directory: {download_dir}")
    
    if key.endswith('/'):
        # It's a directory, so we need to create it
        dir_path = os.path.join(download_dir, key)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    else:
        # It's a file, download it
        file_path = os.path.join(download_dir, key)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"Downloading file: {key} to {file_path}")
        s3_client.download_file(bucket, key, file_path)  
        print(f"Downloaded {key} to {file_path}")

# Directory to save the downloaded files  
download_dir = 'downloads'

# List and download files  
print(f"Start listing objects...")  
objects = list_objects(bucket_name, prefix)

print(f"Found {len(objects)} objects")
for obj in objects:
    print(f"Object Key: {obj['Key']}")  
    download_object(bucket_name, obj['Key'], download_dir)

print("Download complete.")
