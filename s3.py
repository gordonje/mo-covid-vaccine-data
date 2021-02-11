import os
import boto3


S3_CLIENT = boto3.client('s3')
PROJECT_NAME = os.getenv('PROJECT_NAME')


def read_from(key):
    params = {
        'Bucket': PROJECT_NAME,
        'Key': key
    }
    try:
        response = S3_CLIENT.get_object(**params)
    except S3_CLIENT.exceptions.NoSuchKey:
        return None
    else:
        return response['Body'].read()


def write_to(key, content, content_type):
    params = {
        'Bucket': PROJECT_NAME,
        'ACL': 'public-read',
        'Key': key,
        'Body': content,
        'ContentType': content_type
    }
    return S3_CLIENT.put_object(**params)
