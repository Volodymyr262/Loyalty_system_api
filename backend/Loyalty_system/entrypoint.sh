#!/bin/bash

# Exit immediately if any command fails
set -e

# Activate virtual environment
echo "Activating virtual environment..."
source /opt/venv/bin/activate

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2

# Start Gunicorn
echo "Starting Gunicorn..."
exec "$@"
