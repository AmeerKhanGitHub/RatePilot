import requests
import logging
from xml.etree import ElementTree as ET
from sqlalchemy.exc import SQLAlchemyError
from backend.models.models import ForwardCurve, Session
import sys

# Configure logging to stdout and stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def fetch_xml_data(url):
    """Fetch XML data from the provided URL."""
    logging.info(f"Fetching XML data from {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("XML data fetched successfully.")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching XML data: {e}")
        return None

def transform_data(xml_data):
    """Transform XML data into a list of ForwardCurve objects."""
    if xml_data is None:
        logging.warning("No XML data provided for transformation.")
        return []

    logging.info("Transforming XML data.")
    root = ET.fromstring(xml_data)
    records = []

    for row in root.findall(".//Row"):
        reset_date = row.findtext("ResetDate")
        one_month_sofr = row.findtext("ONEMTSOFR")

        if reset_date and one_month_sofr:
            try:
                one_month_sofr_value = round(float(one_month_sofr.replace('%', '').strip()) / 100, 4)
                records.append(ForwardCurve(reset_date=reset_date, one_month_sofr=one_month_sofr_value))
            except ValueError:
                logging.warning(f"Skipping invalid SOFR value: {one_month_sofr}")

    logging.info(f"Transformed data into {len(records)} records.")
    return records

def load_data_to_sqlite(records):
    """Load transformed data into the PostgreSQL database."""
    session = Session()
    try:
        logging.info("Loading data into database.")
        session.query(ForwardCurve).delete()
        session.add_all(records)
        session.commit()
        logging.info(f"Successfully loaded {len(records)} records into the database.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error loading data into database: {e}")
    finally:
        session.close()

def run_etl():
    """Run the ETL process: fetch, transform, and load data."""
    logging.info("Starting ETL process.")
    url = 'https://19621209.fs1.hubspotusercontent-na1.net/hubfs/19621209/FWDCurveTable.xml'
    xml_data = fetch_xml_data(url)
    records = transform_data(xml_data)
    load_data_to_sqlite(records)
    logging.info("ETL process completed.")

if __name__ == '__main__':
    run_etl()
