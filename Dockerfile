# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Chromium
RUN apt-get update && apt-get install -y wget curl unzip gnupg2 build-essential libpq-dev \
    && apt-get install -y chromium

# Install ChromeDriver compatible with the installed Chromium
RUN CHROMIUM_VERSION=$(chromium --version | grep -oP '\d+\.\d+\.\d+\.\d+') \
    && CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMIUM_VERSION) \
    && wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver \
    && chown root:root /usr/local/bin/chromedriver \
    && chmod 0755 /usr/local/bin/chromedriver \
    && rm ~/chromedriver_linux64.zip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /.cache/selenium
RUN chmod -R 777 /.cache/

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]