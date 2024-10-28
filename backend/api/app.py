from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from backend.models.models import ForwardCurve, Session
import logging
import sys

app = Flask(__name__)
CORS(app)

# Configure logging to stdout and stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def get_sofr_rates():
    """Fetch SOFR rates from the database."""
    session = Session()
    try:
        logging.info("Attempting to fetch SOFR rates from the database.")
        rates = session.query(ForwardCurve).order_by(ForwardCurve.reset_date).all()
        if rates:
            logging.info(f"Fetched {len(rates)} SOFR rates.")
        else:
            logging.warning("No SOFR rates found in the database.")
        return [{"reset_date": rate.reset_date, "one_month_sofr": rate.one_month_sofr} for rate in rates]
    except SQLAlchemyError as e:
        logging.error(f"Error fetching SOFR rates: {e}")
        return []
    finally:
        session.close()

def calculate_interest_rate(maturity_date, rate_floor, rate_ceiling, rate_spread):
    """Calculate interest rates based on provided parameters."""
    logging.info("Calculating interest rates with given parameters.")
    try:
        maturity_date_obj = datetime.strptime(maturity_date, "%m/%d/%Y").date()
    except ValueError:
        logging.error("Invalid maturity date format provided.")
        return []

    result = []
    start_date = datetime.now().date()
    while start_date <= maturity_date_obj:
        days_to_maturity = (maturity_date_obj - start_date).days
        rate = max(rate_floor, min(rate_ceiling, rate_floor + rate_spread * (days_to_maturity / 365)))

        result.append({
            "date": start_date.strftime("%m/%d/%Y"),
            "rate": round(rate, 6)
        })

        # Increment start_date by about one month
        start_date += timedelta(days=30)  # Simplified month increment

    logging.info(f"Generated interest rates for {len(result)} months.")
    return result

@app.route('/api/sofr-rates', methods=['GET'])
def fetch_sofr_rates():
    """API endpoint to fetch SOFR rates."""
    logging.info("API endpoint /api/sofr-rates accessed.")
    try:
        rates = get_sofr_rates()
        if not rates:
            logging.warning("No rates returned to API request.")
        return jsonify(rates)
    except Exception as e:
        logging.error(f"Unexpected error in fetch_sofr_rates: {e}")
        return jsonify({"error": "Failed to fetch SOFR rates.", "details": str(e)}), 500

@app.route('/api/calculate-rates', methods=['POST'])
def calculate_rates():
    """API endpoint to calculate interest rates."""
    logging.info("API endpoint /api/calculate-rates accessed.")

    # Parse JSON request data
    data = request.get_json()
    if not data:
        logging.warning("No JSON data provided in request.")
        return jsonify({"error": "Invalid request: JSON data missing."}), 400

    # Validate and extract required parameters
    required_params = ["maturity_date", "rate_floor", "rate_ceiling", "rate_spread"]
    for param in required_params:
        if param not in data:
            logging.warning(f"Missing parameter: {param}")
            return jsonify({"error": f"Missing parameter: {param}"}), 400

    # Attempt to parse parameters and handle any type errors
    try:
        rate_floor = float(data['rate_floor'])
        rate_ceiling = float(data['rate_ceiling'])
        rate_spread = float(data['rate_spread'])
        maturity_date = data['maturity_date']
    except (ValueError, TypeError):
        logging.error("Invalid parameter type for rate_floor, rate_ceiling, or rate_spread.")
        return jsonify({"error": "Invalid parameter type for rate_floor, rate_ceiling, or rate_spread."}), 400

    # Perform rate calculation
    result = calculate_interest_rate(maturity_date, rate_floor, rate_ceiling, rate_spread)

    # Return the result
    if not result:
        logging.warning("No rates calculated due to invalid input or parameters.")
        return jsonify({"error": "Failed to calculate rates due to invalid parameters."}), 400

    return jsonify(result), 200

if __name__ == '__main__':
    logging.info("Starting Flask app.")
    app.run(host='0.0.0.0', port=5000, debug=True)
