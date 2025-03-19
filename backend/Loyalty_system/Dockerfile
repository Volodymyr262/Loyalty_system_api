# Use the official Python image with a slim version for smaller size
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set the working directory in the container
WORKDIR /app

# Copy project files to the container
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev && apt-get clean

# Upgrade pip and install project dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files (important for production)
RUN python manage.py collectstatic --noinput

# Expose the port Railway will use
EXPOSE ${PORT}

# Start Gunicorn server
CMD gunicorn Loyalty_system.wsgi:application --bind 0.0.0.0:${PORT}
