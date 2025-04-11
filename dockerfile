# Use Python base image
FROM python:3.9-slim

# Install system dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev libssl-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variables if needed (optional)
# ENV FLASK_APP=app.py

# Run the app
CMD ["python", "app.py"]
