#!/bin/bash
set -e

docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml build --no-cache
docker-compose -f docker-compose.dev.yml up

echo "Containers em desenvolvimento iniciados!"


