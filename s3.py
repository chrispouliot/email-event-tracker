import boto3
import email

s3 = boto3.resource('s3')


def get_message_from_s3(key: str, bucket: str) -> email.message:
    obj = s3.Object(bucket, key)
    raw_email = obj.get()['Body'].read().decode('utf-8')
    # Turn raw email mimetipe to a mime message to extract content without headers
    message = email.message_from_string(raw_email)
    return message


def save_message_to_s3(key: str, bucket: str, data: str):
    obj = s3.Object(bucket, key)
    obj.put(data)
