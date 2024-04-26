# Stage 1: Install Chromium and ChromeDriver
FROM debian:buster as chromedriver-stage
RUN apt-get update && apt-get install -y wget unzip gnupg2 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

RUN google-chrome --version

# Install the matching version of ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oE "[0-9.]+") \
    && CHROMEDRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") \
    && wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /opt/chromedriver \
    && ln -s /opt/chromedriver/chromedriver /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Stage 2: Python environment with app setup
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the necessary binaries from the first stage
COPY --from=chromedriver-stage /opt/chromedriver /opt/chromedriver
COPY --from=chromedriver-stage /usr/local/bin/chromedriver /usr/local/bin/chromedriver
COPY --from=chromedriver-stage /opt/google/chrome/google-chrome /opt/google/chrome/google-chrome

# Set environment variable for Chrome binary location
ENV CHROME_BIN=/opt/google/chrome/google-chrome

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Setup permissions for Selenium's cache
RUN mkdir -p /.cache/selenium
RUN chmod -R 777 /.cache/

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "808
