#!/bin/sh

git pull
docker build --tag=feinstaub-prod .
docker rm -f feinstaub feinstaub-nginx
docker run -d --volumes-from feinstaub-data --link feinstaub-db:db --restart=always --name feinstaub feinstaub-prod
docker run --name feinstaub-nginx --net="host" --volumes-from feinstaub-data -v `pwd`/nginx.conf:/etc/nginx/nginx.conf --restart=always -d nginx
