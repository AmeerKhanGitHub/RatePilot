# backend/etl/tests/test_etl.py

import unittest
from unittest.mock import patch
from backend.etl.etl import fetch_xml_data, transform_data, load_data_to_sqlite
from backend.models.models import ForwardCurve, Session

class ETLTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests."""
        cls.test_data = '''
            <Root>
                <Row><ResetDate>2024-10-01</ResetDate><ONEMTSOFR>0.15%</ONEMTSOFR></Row>
                <Row><ResetDate>2024-10-02</ResetDate><ONEMTSOFR>0.20%</ONEMTSOFR></Row>
            </Root>'''

    def setUp(self):
        """Setup database for each test."""
        self.session = Session()

    def tearDown(self):
        """Clear the database after each test."""
        self.session.query(ForwardCurve).delete()
        self.session.commit()
        self.session.close()

    @patch('backend.etl.etl.requests.get')
    def test_fetch_xml_data(self, mock_get):
        """Test fetching XML data from a URL."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = self.test_data

        result = fetch_xml_data("https://example.com/fake-url")
        mock_get.assert_called_once()
        self.assertEqual(result, self.test_data)

    def test_transform_data(self):
        """Test transforming XML data to a list of records."""
        records = transform_data(self.test_data)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].reset_date, '2024-10-01')
        self.assertEqual(records[0].one_month_sofr, 0.0015)
        self.assertEqual(records[1].reset_date, '2024-10-02')
        self.assertEqual(records[1].one_month_sofr, 0.0020)

    def test_load_data_to_sqlite(self):
        """Test loading transformed data into SQLite database."""
        records = transform_data(self.test_data)
        load_data_to_sqlite(records)

        # Verify data is loaded correctly
        loaded_records = self.session.query(ForwardCurve).all()
        self.assertEqual(len(loaded_records), 2)
        self.assertEqual(loaded_records[0].reset_date, '2024-10-01')
        self.assertEqual(loaded_records[0].one_month_sofr, 0.0015)
        self.assertEqual(loaded_records[1].reset_date, '2024-10-02')
        self.assertEqual(loaded_records[1].one_month_sofr, 0.0020)

if __name__ == '__main__':
    unittest.main()
