# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the application code to the container
COPY app.py /app

# Install Flask
RUN pip install flask

# Expose the port that Flask will run on
EXPOSE 8080

# Set the command to run the Flask app
CMD ["python", "app.py"]
