
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Installations
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y gcc
RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the app
CMD mkdir /usr/src/app
COPY ./app /usr/src/app

# Make port available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME World

ENTRYPOINT gunicorn --chdir /usr/src/app main:app -w 2 --threads 2 -b 0.0.0.0:80
