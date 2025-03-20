#!/bin/sh

# Exit immediately if a command fails
set -e

echo "Activating virtual environment..."
. /opt/venv/bin/activate  # Use "." instead of "source" for POSIX compliance

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2

echo "Starting Gunicorn..."
exec gunicorn Loyalty_system.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --log-level info
