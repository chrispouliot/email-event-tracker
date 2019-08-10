from datetime import datetime, timedelta
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import encode_base64

from icalendar import Calendar, Event, vText, vCalAddress


def add_event_to_email_mime(start_dt: datetime, title: str, ori_msg: Message) -> Message:
    calendar = Calendar()
    # Required
    calendar.add('prodid', '-//My calendar product//mxm.dk//')
    calendar.add('version', '2.0')

    event = Event()
    event.add('summary', ori_msg.get('Subject'))
    event.add('dtstart', start_dt)
    event.add('dtend', start_dt + timedelta(hours=1))
    event.add('dtstamp', start_dt + timedelta(hours=1))

    attendee = vCalAddress(f"MAILTO:{ori_msg.get('To')}")
    attendee.params['cn'] = vText('Name')
    attendee.params['ROLE'] = vText('REQ-PARTICIPANT')

    event.add('attendee', attendee, encode=0)
    calendar.add_component(event)

    body = ori_msg.get_payload()
    msg = MIMEMultipart('mixed')
    for key in ori_msg.keys():
        msg[key] = ori_msg.get(key)

    part_email = MIMEText(body, "html")
    part_cal = MIMEText(str(calendar.to_ical()), 'calendar;method=REQUEST')

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    ical_atch = MIMEBase('application/ics', ' ;name="invite.ics"')
    ical_atch.set_payload(calendar.to_ical())
    print(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="invite.ics"')

    eml_atch = MIMEBase('text/plain', '')
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msg_alternative.attach(part_email)
    msg_alternative.attach(part_cal)
    return msg_alternative
