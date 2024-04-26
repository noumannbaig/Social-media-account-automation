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

# Install Chromium using the official repository
RUN curl -sSL https://packages.chromium.org/keyring/pool/main/gpg-key-chromium | apt-key add -
# Add the Chromium repository source list
RUN echo "deb [arch=amd64] http://apt.chromium.org/ stable main" >> /etc/apt/sources.list.d/chromium.list

# Update package lists after adding the repository
RUN apt-get update

# Install Chromium and ChromeDriver
RUN apt-get install -y chromium-chromedriver

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Improve security by creating cache directory with limited permissions
RUN mkdir -p /.cache/selenium && chmod 700 /.cache/selenium

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
