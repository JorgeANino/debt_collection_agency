# Use an official Python 3.10 runtime as a parent image
FROM python:3.10-slim-bullseye

# Prevent Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat gcc libpq-dev

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Copy and prepare the entrypoint script directly to the root
COPY deploy/entrypoint.sh /entrypoint.sh

# Fix potential Windows line endings
RUN sed -i 's/\r$//' /entrypoint.sh 

RUN chmod +x /entrypoint.sh

# Inform Docker that the container listens on the specified port at runtime.
EXPOSE 8000

# Define the script you want to run when the container starts.
ENTRYPOINT ["/entrypoint.sh"]
