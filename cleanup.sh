#!/bin/bash
set -e

echo "Stopping all containers..."
docker-compose down -v

echo "Cleaning up directories..."
sudo rm -rf ./logs/*
sudo rm -rf ./scrapy_output/*

echo "Resetting permissions..."
sudo chmod -R 777 ./logs
sudo chmod -R 777 ./scrapy_output
sudo chmod -R 777 ./dags
sudo chmod -R 777 ./plugins

echo "Cleanup complete. You can now run setup.sh again."