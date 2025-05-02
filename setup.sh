#!/bin/bash
set -e

# Create required directories
mkdir -p ./dags ./logs ./plugins ./airflow ./scrapy_output

# Ensure proper permissions for all directories
chmod -R 777 ./logs
chmod -R 777 ./scrapy_output
chmod -R 777 ./dags
chmod -R 777 ./plugins

# Initialize Airflow
docker-compose up airflow-init

# Start all services
docker-compose up -d

echo "========================================"
echo "Airflow is now running!"
echo "Access the Airflow UI at: http://localhost:8080"
echo "Username: airflow"
echo "Password: airflow"
echo "========================================"