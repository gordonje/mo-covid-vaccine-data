import os
import boto3


S3_CLIENT = boto3.client('s3')
PROJECT_NAME = os.getenv('PROJECT_NAME')


def read_all_files():
    params = {
        'Bucket': PROJECT_NAME
    }
    r = S3_CLIENT.list_objects_v2(**params)
    return r['Contents']


def read_object_versions(key):
    params = {
        'Bucket': PROJECT_NAME,
        'Prefix': key
    }
    try:
        response = S3_CLIENT.list_object_versions(**params)
    except S3_CLIENT.exceptions.NoSuchKey:
        return None
    else:
        return response


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
