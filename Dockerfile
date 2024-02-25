# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Install the necessary packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

#
WORKDIR /avatarmanagement

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /avatarmanagement/app

COPY entrypoint.sh /avatarmanagement/app/entrypoint.sh
RUN chmod +x /avatarmanagement/app/entrypoint.sh

#Security
RUN find / -perm 6000 -type f -exec chmod a-s {} \; || true
RUN addgroup --gid 102 phaza\
	&& useradd phaza -u10001 -g102\
	&& usermod -aG phaza phaza
USER phaza

# Make port 8000 available to the world outside this container
EXPOSE 8080
#
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
ENTRYPOINT ["/avatarmanagement/app/entrypoint.sh"]
