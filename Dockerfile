# Dockerfile for Flask
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Flask environment variable
ENV FLASK_APP=run.py

# Expose port for Flask
EXPOSE 5000

# Command to run Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
