import os

from parser import extract_data
from s3 import get_message_from_s3, save_message_to_s3
from mime import add_event_to_email_mime


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

        mime_message = get_message_from_s3(message_id, BUCKET_NAME)
        start_dt, title = extract_data(mime_message.get_payload())
        event_mime_message = add_event_to_email_mime(start_dt, title, mime_message)
        save_message_to_s3(message_id, BUCKET_NAME, event_mime_message)

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
