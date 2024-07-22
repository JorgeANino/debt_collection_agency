#!/bin/bash

# Path to the directory containing the Docker Compose file
COMPOSE_FILE_PATH="docker-compose.yml"

# Stop and remove containers, networks, and volumes
docker-compose -f $COMPOSE_FILE_PATH down

docker rmi $(docker images -a -q)

docker volume rm $(docker volume ls -q)

docker system prune -a -f

docker volume prune -f

# Rebuild the Docker images
docker-compose -f $COMPOSE_FILE_PATH build

# Start the containers in detached mode
docker-compose -f $COMPOSE_FILE_PATH up -d
