# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /backend

# Copy requirements.txt into the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port that Flask is using
EXPOSE 5000

# Run the command to start the Flask server
CMD ["python", "src/main.py", "--host=0.0.0.0"]
