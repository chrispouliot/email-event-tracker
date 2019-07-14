import unittest

from unittest.mock import MagicMock

from handler import get_html_from_s3


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


if __name__ == '__main__':
    unittest.main()
