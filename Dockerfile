
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install necessary packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc && \
    pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the app
COPY ./app /usr/src/app

EXPOSE 8081
WORKDIR /usr/src/app

ENTRYPOINT ["gunicorn", "--chdir", "/usr/src/app", "main:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8081"]
