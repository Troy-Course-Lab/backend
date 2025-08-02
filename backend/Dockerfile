FROM python:3.11-slim-bullseye

WORKDIR /app

# Install system dependencies required for building some Python packages
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy and install Python dependencies
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the application code
COPY ./backend /app/backend

# Copy and make the entrypoint script executable
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh