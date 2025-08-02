#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run migrations
echo "--- Running database migrations ---"
alembic upgrade head

# Create initial data in database
echo "--- Creating initial data ---"
python /app/app/initial_data.py

# Start the application server
echo "--- Starting Uvicorn server ---"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4