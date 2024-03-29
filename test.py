from datetime import datetime
import unittest
from unittest import mock

from handler import get_message_from_s3
from parser import find_date
from mime import add_event_to_email_mime


@mock.patch('s3.s3')
class TestEmailParsing(unittest.TestCase):
    simple_email_dict = {}

    def setUp(self):
        for fname in ['simple1.dms', 'simple_with_ics.dms', 'simple_without_ics.dms']:
            with open(f'fixtures/{fname}', 'r') as file:
                self.simple_email_dict[fname] = file.read(),

    def test_read(self, mock_s3):
        expected = "This is a simple test for your appointment July 21st at 10am\n"
        test_content = self.simple_email_dict['simple1.dms']

        mock_s3.Object.return_value \
            .get.return_value.__getitem__.return_value \
            .read.return_value \
            .decode.return_value = test_content

        returned_value = get_message_from_s3("key", "bucket")
        self.assertEqual(returned_value.get_payload(), expected)

    def test_create_mime(self, mock_s3):
        test_content = self.simple_email_dict['simple_without_ics.dms']
        expected_content = self.simple_email_dict['simple_with_ics.dms']

        mock_s3.Object.return_value \
            .get.return_value.__getitem__.return_value \
            .read.return_value \
            .decode.return_value = test_content

        original_mime = get_message_from_s3("key", "bucket")
        calendar_mime = add_event_to_email_mime(datetime.now(), "title", original_mime)
        self.assertEqual(calendar_mime.as_string(), expected_content.as_string())


class TestDateParsing(unittest.TestCase):

    def setUp(self):
        self.valid_data = [
            ["Your appointment is on 1/2/2019 at 2:30pm", datetime(2019, 2, 1, 14, 30)],
            ["Your booking is for July 1st at 1pm", datetime(2019, 7, 1, 13)],
            ["You have reserved for 11am on September 2nd", datetime(2019, 9, 2, 11)],
        ]

    def test_valid_inputs(self):
        for test, expected in self.valid_data:
            actual = find_date(test)
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
