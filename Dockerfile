# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies for Chromium and Python
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    curl \
    gnupg2 \
    build-essential \
    libpq-dev

# Install dependencies for apt signing
RUN apt-get install -y ca-certificates

# Import the Chromium GPG key from the official Debian packages list
RUN curl -sSL https://packages.debian.org/pool/main/chromium-browser/chromium-browser_stable_amd64.deb.asc | apt-key add -

# Add the Chromium repository source list (replace 'buster' with your Debian version if different)
RUN echo "deb [arch=amd64] http://deb.debian.org/debian buster main" >> /etc/apt/sources.list.d/chromium.list

# Update package lists after adding the repository
RUN apt-get update

# Install Chromium and ChromeDriver (may vary depending on version)
RUN apt-get install -y chromium-chromedriver

# Verify Chromium installation
RUN chromium --version

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Improve security by creating cache directory with limited permissions
RUN mkdir -p /.cache/selenium && chmod 700 /.cache/selenium

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
