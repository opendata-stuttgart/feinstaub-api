#!/bin/sh

set -e

git pull
docker build --tag=feinstaub-prod .
docker rm -f feinstaub feinstaub-nginx
docker run -d -v $(pwd)/../feinstaub-data:/home/uid1000 --link feinstaub-db:db --link feinstaub-redis:redis -v `pwd`/feinstaub/feinstaub/settings/production.py:/opt/code/feinstaub/feinstaub/settings/production.py --restart=always --name feinstaub feinstaub-prod
docker run --name feinstaub-nginx --net="host" -v $(pwd)/../feinstaub-data:/home/uid1000 -v `pwd`/nginx.conf:/etc/nginx/nginx.conf --restart=always -d nginx:1.11

echo "Cleaning up old docker images..."
docker rmi $(docker images | grep "<none>" | awk '{print($3)}')
