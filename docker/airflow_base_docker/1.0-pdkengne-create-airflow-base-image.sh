#!/bin/bash


# exécuter ce fichier dans un terminal à partir de la racine du projet à l'aide des deux commandes suivantes
#-----------------------------------------------------------------------
#chmod +x ./docker/airflow_base_docker/1.0-pdkengne-create-airflow-base-image.sh
#./docker/airflow_base_docker/1.0-pdkengne-create-airflow-base-image.sh
#-----------------------------------------------------------------------


# build image
docker build -t airflow_docker ./docker/airflow_base_docker/


# tag the created image
docker tag airflow_docker:latest march2023mlops/airflow_docker:latest


# log into the Docker public registry
docker login --username march2023mlops --password march2023mlops


# push a new tag to the created image
docker push march2023mlops/airflow_docker:latest


# remove the first created image
docker rmi airflow_docker:latest


# Test the created image
#docker pull march2023mlops/airflow_docker:latest
#docker run --name test -it --rm march2023mlops/airflow_docker:latest
#docker run --name test -it --rm march2023mlops/airflow_docker:latest /bin/bash


