#!/bin/bash
echo "Stopping and removing services..."
docker-compose down -v

if [ $? -ne 0 ]; then
  echo "Failed to stop services."
  exit 1
fi

echo "Services stopped and volumes removed."
