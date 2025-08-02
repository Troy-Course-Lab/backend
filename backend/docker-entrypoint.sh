#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Set Python path to include current directory
export PYTHONPATH=$(pwd):$PYTHONPATH

# Run migrations
echo "--- Running database migrations ---"
alembic upgrade head

# Create initial data in database
echo "--- Creating initial data ---"
python -m app.initial_data

# Start the application server
echo "--- Starting Uvicorn server ---"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4