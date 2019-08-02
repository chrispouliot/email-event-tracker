from datetime import datetime
import unittest
from unittest.mock import MagicMock

from handler import get_html_from_s3
from parser import find_date


class TestEmailRetrieval(unittest.TestCase):

    def setUp(self):
        with open('fixtures/simple1.dms', 'r') as file:
            self.simple_email_dict = {
                'content': file.read(),
                'expected': "This is a simple test for your appointment July 21st at 10am\n",
            }

    def test_read(self):
        expected = self.simple_email_dict['expected']
        test_content = self.simple_email_dict['content']

        mock_s3 = MagicMock()
        mock_s3.Object.return_value \
            .get.return_value.__getitem__.return_value \
            .read.return_value \
            .decode.return_value = test_content

        returned_value = get_html_from_s3("key", "bucket", mock_s3)
        self.assertEqual(returned_value, expected)


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
