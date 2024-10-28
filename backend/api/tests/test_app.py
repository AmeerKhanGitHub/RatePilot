import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from io import StringIO
import logging
import json
from backend.api.app import app

# Define a simple ForwardCurve mock class
class MockForwardCurve:
    def __init__(self, reset_date, one_month_sofr):
        self.reset_date = reset_date
        self.one_month_sofr = one_month_sofr

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the Flask testing client and a temporary log handler."""
        self.app = app.test_client()
        self.app.testing = True

        # Set up an in-memory log stream for testing
        self.log_stream = StringIO()
        logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(self.log_stream)])

    @patch('backend.api.app.Session')  # Mock the Session used in calculate_interest_rate
    @patch('backend.api.app.logging')
    def test_valid_request(self, mock_logging, mock_session):
        """Test a valid request to the calculate-rates endpoint with mocked logging and session."""
        mock_logging.info = MagicMock()

        # Configure mock session to return specific rate data
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = [
            MockForwardCurve(datetime(2024, 12, 31).date(), 0.03),
            MockForwardCurve(datetime(2025, 1, 31).date(), 0.035),
            MockForwardCurve(datetime(2025, 2, 28).date(), 0.04),
        ]
        mock_session.return_value.query.return_value = mock_query

        # Define test payload
        payload = {
            "maturity_date": "02/02/2025",
            "rate_floor": 0.01,
            "rate_ceiling": 0.05,
            "rate_spread": 0.02
        }

        # Make POST request to the API endpoint
        response = self.app.post('/api/calculate-rates',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        # Validate response
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIsInstance(response_json, list)
        self.assertEqual(len(response_json), 3)  # Should have 3 rates as defined above
        self.assertIn('date', response_json[0])
        self.assertIn('rate', response_json[0])

        # Check logging call
        mock_logging.info.assert_called()

    @patch('backend.api.app.Session')
    @patch('backend.api.app.logging')
    def test_invalid_request_missing_parameter(self, mock_logging, mock_session):
        """Test for a request missing a required parameter with mocked logging."""
        # Mock logging configuration
        mock_logging.warning = MagicMock()

        # Define payload with a missing 'rate_spread'
        payload = {
            "maturity_date": "02/02/2025",
            "rate_floor": 0.01,
            "rate_ceiling": 0.05
        }

        # Make POST request to the API endpoint
        response = self.app.post('/api/calculate-rates',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        # Validate response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Missing parameter: rate_spread"})

        # Check logging call
        mock_logging.warning.assert_called_with("Missing parameter: rate_spread")

    @patch('backend.api.app.Session')
    @patch('backend.api.app.logging')
    def test_invalid_request_type_error(self, mock_logging, mock_session):
        """Test for a request with incorrect parameter types with mocked logging."""
        # Mock logging configuration
        mock_logging.error = MagicMock()

        # Define payload with incorrect type for 'rate_floor'
        payload = {
            "maturity_date": "02/02/2025",
            "rate_floor": "not_a_number",  # Invalid type
            "rate_ceiling": 0.05,
            "rate_spread": 0.02
        }

        # Make POST request to the API endpoint
        response = self.app.post('/api/calculate-rates',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        # Validate response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid parameter type for rate_floor, rate_ceiling, or rate_spread."})

        # Check logging call
        mock_logging.error.assert_called_with("Invalid parameter type for rate_floor, rate_ceiling, or rate_spread.")


if __name__ == '__main__':
    unittest.main()
