import boto3

import os

from datetime import datetime

# Lambda scoped
s3 = boto3.resource('s3')
BUCKET_NAME = os.environ.get('bucket_name')

SESInput = {
    "Records": [{
        "eventSource": "",
        "eventVersion": "",
        "ses": {
            "receipt": {},
            "mail": {
                "destination": "",
                "messageId": "",
                "source": "",
                "timestamp": "",
                "headers": "",
                "commonHeaders": {
                    "subject": "",
                },
                "headersTruncated": "",
            },
        },
    }]
}


def handler(events: SESInput, context):
    for event in events.get('Records', []):
        message_id, subject = get_id_and_subject(event)

        if not is_subject_event_related(subject):
            print(f"Subject '{subject}' is not related to an event, skipping'")
            continue

        if not message_id:
            print("No messageID found")
            continue

        email = get_email(message_id, BUCKET_NAME, s3)
        start_dt, end_dt, title = extract_data(email)
        add_to_calendar(start_dt, end_dt, title)
    print("Exiting")


def get_id_and_subject(event: dict) -> (str, str):
    mail = event['ses']['mail']
    return mail['messageId'], mail['commonHeaders']['subject']


def is_subject_event_related(subject: str) -> bool:
    keywords = [
        'appointment',
        'attend',
        'booking',
        'event',
        'flight',
        'invite',
        'meeting',
        'reservation',
    ]
    return any([k in subject.lower() for k in keywords])


def get_email(key: str, bucket: str, s3: boto3.resources.base.ServiceResource) -> str:
    obj = s3.Object(bucket, key)
    return obj.get()['Body'].read().decode('utf-8')


def extract_data(email: str) -> (datetime, datetime, str):
    pass


def add_to_calendar(start_dt: datetime, end_dt: datetime, title: str):
    pass
