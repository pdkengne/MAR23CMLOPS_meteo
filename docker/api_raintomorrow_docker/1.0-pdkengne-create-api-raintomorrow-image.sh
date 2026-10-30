#!/bin/bash


# exécuter ce fichier dans un terminal à partir de la racine du projet à l'aide des deux commandes suivantes
#-----------------------------------------------------------------------
#chmod +x ./docker/api_raintomorrow_docker/1.0-pdkengne-create-api-raintomorrow-image.sh
#./docker/api_raintomorrow_docker/1.0-pdkengne-create-api-raintomorrow-image.sh
#-----------------------------------------------------------------------


# build image
docker build -t api_raintomorrow ./docker/api_raintomorrow_docker/


# tag the created image
docker tag api_raintomorrow:latest march2023mlops/api_raintomorrow:latest


# log into the Docker public registry
docker login --username march2023mlops --password march2023mlops


# push a new tag to the created image
docker push march2023mlops/api_raintomorrow:latest


# remove the first created image
docker rmi api_raintomorrow:latest


# Test the created image
#docker pull march2023mlops/api_raintomorrow:latest
#docker run --name test -p 8000:8000 -it --rm march2023mlops/api_raintomorrow:latest
#docker run --name test -p 8000:8000 --rm api_raintomorrow:latest

# visit: http://localhost:8000/docs
