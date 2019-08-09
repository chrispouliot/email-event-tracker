from datetime import datetime
import re

from bs4 import BeautifulSoup


months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]


def extract_data(html: str) -> (datetime, str):
    soup = BeautifulSoup(html)
    text = soup.get_text()
    return find_date(text), soup.title


# TODO: Refactor this to not be gross
def find_date(text: str) -> datetime:
    text = text.lower()
    minute, hour, day, month, year = 0, 0, 0, 0, 0

    date_match = re.search(r'(\d+/\d+/\d+)', text)

    if date_match:
        date_list = date_match.group().split('/')
        # why cant I use *date_list here??
        day, month, year = date_list[0], date_list[1], date_list[2]
    else:
        # Find format of "July 1st at 1pm"
        month_match = re.findall(r"(?=(" + '|'.join(months) + r"))", text)
        if not month_match:
            # Could not find any month
            return None
        # Take the month, find the index in the list of months, add 1 for 1-12
        month = months.index(month_match[0]) + 1
        # Get the date of the month
        day_match = re.search(r"(\d{1,2})(?:th|st|nd|rd)", text)
        if not day_match:
            return None
        day = day_match.group(1)
        # todo: this year thing wont work near end of year, find closest date with next year too
        year = datetime.now().year

    time_match = re.findall(r'\d{1,2}(?:(?:am|pm)|(?::\d{1,2})(?:am|pm)?)', text)
    if time_match:
        hour, minute = get_time_from_str(time_match[0])

    return datetime(int(year), int(month), int(day), hour, minute)


def get_time_from_str(time_str) -> (int, int):
    postfix = 'pm'
    if 'am' in time_str:
        postfix = 'am'

    time = time_str.split(postfix)[0]
    hour = time
    minute = 0

    if ':' in time:
        hour, minute = time.split(':')

    hour, minute = int(hour), int(minute)

    # convert to 24hour time
    if postfix == 'pm':
        if hour != 12:
            hour = hour + 12
    elif hour == 12:  # If it's midnight AM, set to 0
        hour = 0

    return hour, minute
