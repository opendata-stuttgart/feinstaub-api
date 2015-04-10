#!/bin/sh

set -e

git pull
docker build --tag=feinstaub-prod .
docker rm -f feinstaub feinstaub-nginx
docker run -d --volumes-from feinstaub-data --link feinstaub-db:db --link feinstaub-redis:redis --restart=always --name feinstaub feinstaub-prod
docker run --name feinstaub-nginx --net="host" --volumes-from feinstaub-data -v `pwd`/nginx.conf:/etc/nginx/nginx.conf --restart=always -d nginx

echo "Cleaning up old docker images..."
docker rmi $(docker images | grep "<none>" | awk '{print($3)}')
