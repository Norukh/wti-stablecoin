# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /backend/src

# Copy requirements.txt into the container
COPY requirements.txt /backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /backend/requirements.txt

# Copy the entire project directory into the container
COPY . /backend

# Expose the port that Flask is using
EXPOSE 5000

# Run the command to start the Flask server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]
