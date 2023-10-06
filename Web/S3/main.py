from minio import Minio

import glob
from os import environ


HOST = environ.get("S3_HOST")
PORT = environ.get("S3_PORT")
BUCKET = environ.get("S3_BUCKET")

# generate in MimIO web console [localhost/access-keys]
ACCESS_KEY = environ.get("S3_ACCESS_KEY")
SECRET_KEY = environ.get("S3_SECRET_KEY")
SECURE = int(environ.get("S3_SECURE")) # Http -> False[0], Https -> True[1]

UPLOAD_PREFIX = "upload"

client = Minio(f"{HOST}:{PORT}",
                access_key = ACCESS_KEY,
                secret_key = SECRET_KEY,
                secure = SECURE)

def create_bucket():
    found = client.bucket_exists(BUCKET)

    if not found:
        client.make_bucket(BUCKET)
        print(f"Create bucket '{BUCKET}'")
    else:
        print(f"Bucket '{BUCKET}' already exists")

def _get_files(path):
    return glob.glob(f"{path}*")

def create_resources(path):
    print(f"Upload path: {path}")
    full_path = f"source/{path}/"
    path_len = len(full_path)

    files = _get_files(full_path)

    for i in files:
        name = i[path_len:]
        print(f"\tUpload {name}")
        client.fput_object(bucket_name = BUCKET, object_name = f"{path}/{name}",
                            file_path = f"./{full_path}/{name}")

def upload_object(path, name, data):
    client.put_object(bucket_name = BUCKET, object_name = f"{UPLOAD_PREFIX}/{path}/{name}",
                        data = data, length = -1, part_size=10*1024*1024,)

def get_object(name):
    response = client.get_object(bucket_name = BUCKET, object_name = name)
    return response


if __name__ == "__main__":
    create_bucket()

    # Static resources
    create_resources("img")
    create_resources("fonts")

    # Test data
    create_resources("upload/products")

    # Get file as byte stream
    print(get_object("img/favicon.png"))

    # Upload img as byte stream
    # with open("source/test_files/test_2.jpeg", 'rb') as f:
    #     upload_object("products", "105.jpeg", f)