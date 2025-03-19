# Use a full Python image instead of slim to avoid missing tools
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev

# Install pip manually to avoid issues
RUN python -m ensurepip && python -m pip install --upgrade pip

# Copy the project files
COPY . /app/

# Install project dependencies
RUN pip install -r requirements.txt

# Expose the port for the application
EXPOSE ${PORT}

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script before running Gunicorn
ENTRYPOINT ["/entrypoint.sh"]

# Start Gunicorn server
CMD ["gunicorn", "Loyalty_system.wsgi:application", "--bind", "0.0.0.0:8000"]
