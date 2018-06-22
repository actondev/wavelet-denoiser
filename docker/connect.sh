#!/bin/bash

# example usage: ./connect.sh front
# it will connect to the (eg) data_front_1 container

function getImage {
  target=$1
  match=".*$target.*"
  images=$(sudo docker-compose images)
  echo "$images" |  while read line
  do
    containerName=`echo $line | awk '{print $1}'`
    if [[ $containerName =~ $match ]]; then
        echo $containerName
        return 0
      fi 
  done

}

matchedImage=$(getImage $1)
sudo docker exec -it $matchedImage /bin/bash
