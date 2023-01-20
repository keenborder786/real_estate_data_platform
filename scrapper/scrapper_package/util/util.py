"""

This module have helper functions for the scrapper

"""

from minio import Minio
def bucket_creation(bucket_name:str, client:Minio):
    """
    Create Minio Bucket

    Parameters:
    ----------------------------
    bucket_name(str): The name of the bucket which you would like to create.

    client(Minio): Main client to interact with Minio

    Returns:
    ----------------------------
    None
    
    """
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Bucket has been created")
    else:
        print("Bucket already exists")