#!/bin/bash
set -e


cd /opt/d_12_03_self_storage
git fetch
git pull

cd /opt/d_12_03_self_storage/infra
docker compose -f docker-compose.prod.yml --build up -d

echo selft-storage was updated and it will work soon!
