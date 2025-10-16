# Dockerfile
# Use a standard Python base image. Choose a version that matches your needs.
# Alpine images are smaller, but debian-slim is also good and often has apt.
# Dockerfile
FROM python:3.10-bullseye # Changed from -slim-bullseye

# Install ffmpeg and any other system dependencies
# Using 'apt-get' inside a Dockerfile's RUN command is perfectly fine.
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy your requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Define the command to run your bot when the container starts
CMD ["python", "main.py"]
