# backend/api/Dockerfile
FROM python:3.9-slim

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . ./backend

# Run ETL as part of build
RUN python backend/etl/etl.py

# Run tests
RUN pytest backend/etl/tests/ backend/api/tests/


# Expose port and run server
EXPOSE 5000
CMD ["python", "backend/api/app.py"]
