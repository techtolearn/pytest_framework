import json
from datetime import time

import pytest
import requests


class Utility:

    @staticmethod
    def measure_time(function):
        start = time()
        result = function()
        end = time()
        return end - start, result

    # Utility function to make an API request
    @staticmethod
    def make_api_request(url, method='GET', headers=None, data=None):
        """
        Makes an API request.

        Args:
            url (str): The URL of the API endpoint.
            method (str): The HTTP method (GET, POST, PUT, DELETE, etc.).
            headers (dict): Optional headers to include in the request.
            data: Optional data to include in the request body.

        Returns:
            requests.Response: The response object.
        """
        method = method.upper()
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return response

    @pytest.fixture
    def get_request(self):
        def _send_get_request(url, headers=None, params=None):
            """
            Send a GET request to the specified URL with optional headers and parameters.

            Parameters:
            - url (str): The URL to send the GET request to.
            - headers (dict): Optional dictionary of headers to include in the request.
            - params (dict): Optional dictionary of query parameters to include in the request.

            Returns:
            - requests.Response: The response object.
            """
            response = requests.get(url, headers=headers, params=params)
            return response

        return _send_get_request

    @staticmethod
    def send_post_request(url, json=None, headers=None):
        """
        Send a POST request to the specified URL with optional JSON payload and headers.

        Parameters:
        - url (str): The URL to send the POST request to.
        - json (dict): Optional JSON payload to include in the request body.
        - headers (dict): Optional dictionary of headers to include in the request.

        Returns:
        - requests.Response: The response object.
        """
        response = requests.post(url, json=json, headers=headers)
        return response

    @staticmethod
    def send_put_request(url, json=None, headers=None):
        """
        Send a PUT request to the specified URL with optional JSON payload and headers.

        Parameters:
        - url (str): The URL to send the PUT request to.
        - json (dict): Optional JSON payload to include in the request body.
        - headers (dict): Optional dictionary of headers to include in the request.

        Returns:
        - requests.Response: The response object.
        """
        response = requests.put(url, json=json, headers=headers)
        return response

    @staticmethod
    def send_delete_request(url, headers=None):
        """
        Send a DELETE request to the specified URL with optional headers.

        Parameters:
        - url (str): The URL to send the DELETE request to.
        - headers (dict): Optional dictionary of headers to include in the request.

        Returns:
        - requests.Response: The response object.
        """
        response = requests.delete(url, headers=headers)
        return response

    @staticmethod
    def parse_json(response):
        """
        Parse JSON data from the response object.

        Parameters:
        - response (requests.Response): The response object from the API request.

        Returns:
        - dict: The parsed JSON data.
        """
        try:
            json_data = response.json()
            return json_data
        except ValueError as e:
            print(f"Failed to parse JSON data: {e}")
            return None

    @staticmethod
    def assert_json_response(response, expected_data):
        """
        Asserts that the JSON response matches the expected data.

        Args:
            response (requests.Response): The response object containing the JSON data.
            expected_data (dict): The expected JSON data.
        """
        # Convert response content to JSON
        response_data = response.json()

        # Compare response data with expected data
        assert response_data == expected_data, f"Response data {response_data} does not match expected data {expected_data}"

    @staticmethod
    def assert_json_equal(response1, response2):
        """
        Asserts that two JSON responses are equal.

        Args:
            response1 (dict): The first JSON response.
            response2 (dict): The second JSON response.
        """
        assert response1 == response2, f"JSON responses are not equal:\n{json.dumps(response1, indent=4)}\n{json.dumps(response2, indent=4)}"
