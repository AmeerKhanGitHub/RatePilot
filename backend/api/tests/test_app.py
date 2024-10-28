import unittest
from unittest.mock import patch, MagicMock
import logging
import json
from io import StringIO
from backend.api.app import app  # Import the app from your Flask application file

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the Flask testing client and a temporary log handler."""
        self.app = app.test_client()
        self.app.testing = True

        # Set up an in-memory log stream for testing to stdout
        self.log_stream = StringIO()
        logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(self.log_stream)])

    @patch('backend.api.app.logging')
    def test_valid_request(self, mock_logging):
        """Test a valid request to the calculate-rates endpoint with mocked logging."""
        mock_logging.info = MagicMock()

        payload = {
            "maturity_date": "12/31/2024",
            "rate_floor": 0.01,
            "rate_ceiling": 0.05,
            "rate_spread": 0.02
        }

        response = self.app.post('/api/calculate-rates',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('date', response.get_json()[0])
        self.assertIn('rate', response.get_json()[0])

        mock_logging.info.assert_called()

    @patch('backend.api.app.logging')
    def test_invalid_request_missing_parameter(self, mock_logging):
        """Test for a request missing a required parameter with mocked logging."""
        mock_logging.warning = MagicMock()

        payload = {
            "maturity_date": "12/31/2024",
            "rate_floor": 0.01,
            "rate_ceiling": 0.05
        }

        response = self.app.post('/api/calculate-rates',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Missing parameter: rate_spread"})

        mock_logging.warning.assert_called_with("Missing parameter: rate_spread")

    @patch('backend.api.app.logging')
    def test_invalid_request_type_error(self, mock_logging):
        """Test for a request with incorrect parameter types with mocked logging."""
        mock_logging.error = MagicMock()

        payload = {
            "maturity_date": "12/31/2024",
            "rate_floor": "not_a_number",
            "rate_ceiling": 0.05,
            "rate_spread": 0.02
        }

        response = self.app.post('/api/calculate-rates',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid parameter type for rate_floor, rate_ceiling, or rate_spread."})

        mock_logging.error.assert_called_with("Invalid parameter type for rate_floor, rate_ceiling, or rate_spread.")

    def tearDown(self):
        """Clean up after each test."""
        self.log_stream.close()

if __name__ == '__main__':
    unittest.main()
