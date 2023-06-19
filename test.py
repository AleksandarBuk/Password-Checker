import unittest
from unittest import mock
import hashlib
import requests

import checkmypass


class TestCheck(unittest.TestCase):

    def test_request_api_data(self):
        query_char = 'e.g.'
        expected_url = 'https://api.pwnedpasswords.com/range/e.g.'
        expected_response = requests.Response()
        expected_response.status_code = 200

        with mock.patch('requests.get', return_value=expected_response) as mock_get:
            response = checkmypass.request_api_data(query_char)

            mock_get.assert_called_with(expected_url)
            self.assertEqual(response, expected_response)

    def test_get_password_leaks_count(self):
        hashes = requests.Response()
        hashes._content = b'hash1:10\nhash2:5\nhash3:0'

        count = checkmypass.get_password_leaks_count(hashes, 'hash2')

        self.assertEqual(count, '5')

    def test_pwned_api_check(self):
        password = 'password123'
        sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        first5_char = sha1password[:5]
        tail = sha1password[5:]

        print(f'sha1password: {sha1password}')
        print(f'first5_char: {first5_char}')
        print(f'tail: {tail}')

        expected_response = requests.Response()
        expected_response._content = b'hash1:10\nhash2:5\nhash3:0'

        with mock.patch('checkmypass.request_api_data', return_value=expected_response) as mock_request:
            count = checkmypass.pwned_api_check(password)

            mock_request.assert_called_with(first5_char)
            self.assertEqual(count, 0)

        print(f'Count: {count}')
        print(f'Expected Response Content: {expected_response._content.decode()}')

if __name__ == '__main__':
    unittest.main()
