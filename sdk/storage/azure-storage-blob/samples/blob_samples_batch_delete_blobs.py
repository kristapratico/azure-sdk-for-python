from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
import os
import sys

"""
FILE: blob_samples_batch_delete_blobs.py
DESCRIPTION:
    This sample demonstrates batch deleting blobs from a container.
USAGE:
    python blob_samples_batch_delete_blobs.py
    Set the environment variables with your own values before running the sample:
    1) STORAGE_CONNECTION_STRING - the connection string to your storage account
"""

current_dir = os.path.dirname(os.path.abspath(__file__))
SOURCE_FOLDER = os.path.join(current_dir, "./sample-blobs/")


def batch_delete_blobs_sample(local_path):
    # Set the connection string and container name values to initialize the Container Client
    connection_string = os.getenv('STORAGE_CONNECTION_STRING')

    if connection_string is None:
        print("Missing required environment variable: STORAGE_CONNECTION_STRING." + '\n' +
              "Test: batch_delete_blobs_sample")
        sys.exit(1)

    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
    # Create a ContainerClient to use the batch_delete function on a Blob Container
    container_client = blob_service_client.get_container_client("mycontainername")
    try:
        container_client.create_container()
    except ResourceExistsError:
        pass
    # Upload blobs
    for filename in os.listdir(local_path):
        with open(local_path+filename, "rb") as data:
            container_client.upload_blob(name=filename, data=data, blob_type="BlockBlob")

    # List blobs in storage account
    blob_list = [b.name for b in list(container_client.list_blobs())]

    # Delete blobs
    container_client.delete_blobs(*blob_list)

if __name__ == '__main__':
    batch_delete_blobs_sample(SOURCE_FOLDER)

