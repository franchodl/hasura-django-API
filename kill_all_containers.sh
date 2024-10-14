#!/bin/bash

# Function to stop and remove all Docker containers
stop_and_remove_all_containers() {
  echo "Stopping and removing all Docker containers..."

  # Stop Docker Compose containers
  docker-compose down -v
  
  # Stop and remove other containers if needed
  container_ids=$(docker ps -aq)
  if [ ! -z "$container_ids" ]; then
    docker stop $container_ids
    docker rm $container_ids
  fi

  echo "All Docker containers have been stopped and removed."
}

# Function to remove any unused Docker networks
remove_unused_networks() {
  echo "Removing unused Docker networks..."
  docker network prune -f
  echo "Unused Docker networks have been removed."
}

# Execute the functions
stop_and_remove_all_containers
remove_unused_networks
