#!/bin/bash

# sudo docker-compose stop $1
# sudo docker-compose kill $1
# sudo docker-compose up -d --no-deps $1

sudo docker-compose up -d --no-deps --build --force-recreate $1

# sudo docker-compose build $1
# sudo docker-compose restart $1
