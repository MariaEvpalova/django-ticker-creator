# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt /code/

# Install the required dependencies
RUN pip install -r requirements.txt

# Install ImageMagick
RUN apt-get update && apt-get install -y imagemagick

# Copy the Django project code to the container
COPY . /code/

# Set environment variables for the database
ENV DOCKER=True
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
