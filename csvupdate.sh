#!/bin/bash

cd /home/feinstaub/feinstaub-api
/home/feinstaub/bin/docker-compose run web reset_db --noinput
zcat /home/feinstaub/dbbackup/`date +%Y-%m-%d`.pgdump.gz | /home/feinstaub/bin/docker-compose run db psql -h db -U postgres feinstaub
/home/feinstaub/bin/docker-compose run web export_as_csv
/home/feinstaub/bin/docker-compose stop
docker rmi $(docker images | grep "<none>" | awk '{print($3)}')
