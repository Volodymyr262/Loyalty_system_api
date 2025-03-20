#!/bin/sh

# Exit on any error
set -e

echo "Starting the container..."

echo "Activating virtual environment..."
. /opt/venv/bin/activate  # POSIX-compliant alternative to `source`

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
gunicorn Loyalty_system.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --log-level info &

# Wait for Gunicorn to start (5 seconds)
sleep 5

echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2

echo "Static files collected. Container is fully running."

# Keep the container alive
wait
