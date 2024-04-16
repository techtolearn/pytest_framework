import unittest

import pytest
import requests
from api.utility import Utility


class GetRequest(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Utility class
        self.util = Utility()

    @pytest.fixture
    def base_url(self):
        return "http://example.com/api"

    def test_get_user_details(self, base_url, auth_token):
        # Construct the URL for the API endpoint
        url = f"{base_url}/user/details"

        # Define headers with authentication token
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }

        # Make the API request
        response = self.util.make_api_request(url, headers=headers)

        # Check if the request was successful (status code 200)
        assert response.status_code == 200

        # Parse the JSON response
        response_data = response.json()

        # Perform assertions on the response data
        assert 'user_id' in response_data
        assert 'username' in response_data

    @staticmethod
    def test_example(self, base_url):
        base_url = "https://api.example.com/resource"
        response = self.util.get_request(base_url)
        assert response.status_code == 200
        assert "example" in response.json()["data"]
        expected_data = {
            "key1": "value1",
            "key2": "value2",
            # Add more expected data as needed
        }
        self.util.assert_json_response(response, expected_data)

    def test_getJSonData(self):
        # Example GET request
        get_response = requests.get("https://api.example.com/data")
        assert get_response.status_code == 200
        get_data = self.util.parse_json(get_response)
        assert get_data is not None
        assert "key" in get_data

        # Example POST request
        post_response = requests.post("https://api.example.com/data", json={"key": "value"})
        assert post_response.status_code == 201
        post_data = self.util.parse_json(post_response)
        assert post_data is not None
        assert "key" in post_data

    @staticmethod
    def test_api_response():
        # Assume we have made an API request and got a response object
        response = requests.get('https://api.example.com/data')

        # Define the expected JSON data
        expected_data = {
            "key1": "value1",
            "key2": "value2",
            # Add more expected data as needed
        }

    def test_compare_json_responses(self):
        response1 = {
            "id": 1,
            "name": "John",
            "age": 30,
            "city": "New York"
        }

        response2 = {
            "id": 1,
            "name": "John",
            "age": 30,
            "city": "New York"
        }

        self.util.assert_json_equal(response1, response2)
