# Use full Python image to avoid missing tools
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev

# Install pip manually
RUN python -m ensurepip && python -m pip install --upgrade pip

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the project files
COPY . /app/

# Install project dependencies inside the virtual environment
RUN pip install -r requirements.txt

# Expose the port for the application
EXPOSE ${PORT}

# Start the application using the Procfile command
CMD ["gunicorn", "Loyalty_system.wsgi:application", "--bind", "0.0.0.0:8000"]
