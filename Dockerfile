
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED True
ENV FLASK_DEBUG 0

# Install necessary packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc && \
    pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create a non-root user and change the ownership of the relevant directories
RUN useradd -m myuser && \
    mkdir -p /usr/src/app && \
    chown -R myuser:myuser /usr/src/app

# Copy the app using the non-root user
COPY --chown=myuser:myuser ./app /usr/src/app

# Final setup
EXPOSE 8081
WORKDIR /usr/src/app
USER myuser

ENTRYPOINT ["gunicorn", "--chdir", "/usr/src/app", "main:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8081"]
