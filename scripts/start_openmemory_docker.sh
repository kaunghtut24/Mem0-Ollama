#!/usr/bin/env bash
set -e
echo "This script demonstrates starting OpenMemory with docker-compose using the included override."

# This is a helper. It expects you already have Docker and docker-compose installed.
docker compose -f docker/openmemory.docker-compose.yml up -d
echo "OpenMemory containers should be starting. Check with: docker compose -f docker/openmemory.docker-compose.yml ps"
