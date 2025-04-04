# migrate_media.py (Standalone Script)

import os
import boto3
from django.conf import settings
from decouple import config
if __name__ == "__main__":
    # Replace 'your_project.settings' with the actual path to your settings file
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flix.settings")
    import django
    django.setup()

    session = boto3.session.Session()
    client = session.client(
        's3',
        endpoint_url=config('AWS_S3_ENDPOINT_URL'),
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        region_name='nyc3'
    )

    local_media_root = settings.MEDIA_ROOT
    bucket_name = config('AWS_STORAGE_BUCKET_NAME')
    cloud_media_location = 'media'  # Should match your STORAGES setting

    uploaded_count = 0
    error_count = 0

    for root, _, files in os.walk(local_media_root):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_media_root)
            cloud_key = os.path.join(cloud_media_location, relative_path).replace("\\", "/")

            try:
                client.upload_file(local_path, bucket_name, cloud_key, ExtraArgs={'ACL': 'public-read'}) # Adjust ACL if needed
                print(f'Uploaded {local_path} to s3://{bucket_name}/{cloud_key}')
                uploaded_count += 1
            except Exception as e:
                print(f'Error uploading {local_path}: {e}')
                error_count += 1

    print("\nMigration Summary:")
    print(f"Successfully uploaded: {uploaded_count} files")
    print(f"Errors encountered: {error_count} files")