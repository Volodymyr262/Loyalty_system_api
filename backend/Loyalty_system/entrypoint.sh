#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate virtual environment
echo "Activating virtual environment..."
source /opt/venv/bin/activate

# Run database migrations

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn Loyalty_system.wsgi:application --bind 0.0.0.0:${PORT}
