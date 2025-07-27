#!/bin/bash
echo "Starting services..."
docker-compose up --build -d

if [ $? -ne 0 ]; then
  echo "Failed to start services."
  exit 1
fi

echo "Services are running."
