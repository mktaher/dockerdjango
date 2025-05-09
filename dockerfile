# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /venv

# Activate virtual environment and install Python dependencies
COPY requirements.txt .
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for Django
EXPOSE 8000

# Command to run the application (will be overridden in docker-compose.yml)
CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]