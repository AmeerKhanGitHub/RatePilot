# Loan Calculation Dashboard

A web-based dashboard for calculating loan interest rates based on parameters such as maturity date, rate floor, rate ceiling, and spread. This project includes a Flask-based backend for fetching and calculating rates and a React frontend for user interaction and chart visualization.

## Project Structure

- **backend**: A Flask app that calculates and returns SOFR-based loan interest rates.
   - **models**: SQLAlchemy models defining the `ForwardCurve` table.
   - **ETL scripts**: Scripts for extracting, transforming, and loading SOFR data.
- **frontend**: A React app for user input and displaying calculated rates in a chart.

## Prerequisites

- Docker
- Node.js & npm (for local frontend development)
- Python & pip (for local backend development)
- PostgreSQL (for backend database)

## Setup and Running with Docker

1. **Create a `.env` file** in the root directory with environment variables for PostgreSQL:
   ```plaintext
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_db

2. **Start the services** with Docker Compose:
    ```bash 
   docker-compose up --build
The backend will be available at http://localhost:5000 and the frontend at http://localhost:3000.

## Local Development

### Backend
1. **Install Python dependencies:**
   ```bash
   pip install -r backend/requirements.txt

2. **Set up the database (SQLite for development):**
   ```bash
   export DATABASE_URL=sqlite:///test.db

3. **Run the Flask server:**
   ```bash
   python backend/api/app.py

### Frontend
1. **Install frontend dependencies:**
   ```bash
   cd frontend 
   npm install

2. **Start the React development server:**
   ```bash
   export DATABASE_URL=sqlite:///test.db

## API Endpoints

- **GET /api/sofr-rates**  
  Fetches the stored SOFR rates.

- **POST /api/calculate-rates**  
  Calculates interest rates based on JSON parameters:
   - `maturity_date`: Target date for maturity.
   - `rate_floor`: Minimum rate value.
   - `rate_ceiling`: Maximum rate value.
   - `rate_spread`: Rate spread per year.



## Running Tests

### Backend Tests
1. **Run the backend tests with:**
   ```bash
   pytest backend/etl/tests/ backend/api/tests/ 

###  Frontend Tests:
1. **Run the following command to execute frontend tests:**
   ```bash
   cd frontend 
   npm test

## Project Details

- **Backend**: Flask, SQLAlchemy, and PostgreSQL for data handling.
- **Frontend**: React with Chart.js for visualizing rate calculations.
- **ETL**: Processes XML data to load SOFR rates into the database.

### Time Spent
- Total Time: Approximately 6 hours

### Areas for Improvement or Further Consideration

1. **Security**:
   - Integrate security measures such as input validation, data sanitization, and authentication/authorization for API endpoints.

2. **Scalability**:
   - Optimize the backend to handle increased load, possibly by implementing caching mechanisms or using a more scalable database solution.

3. **Performance Monitoring**:
   - Set up performance monitoring tools to track application performance and identify bottlenecks.

4. **Deployment**:
   - Consider using CI/CD pipelines for automated testing and deployment to streamline the release process.

5. **User Interface Enhancements**:
   - Improve the frontend UI/UX for better user engagement and accessibility features.

6. **Data Integrity**:
   - Implement mechanisms to ensure data integrity, such as transactional support during ETL processes.

7. **Logging**:
   - Incorporate logging for better traceability and debugging, especially for production environments.

