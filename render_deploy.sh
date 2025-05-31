#!/bin/bash

# This script initializes the database schema for the Food Delivery App on Render

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Run the initialization script
echo "Initializing database schema..."
psql $DATABASE_URL -f init.sql

echo "Database initialization completed"
