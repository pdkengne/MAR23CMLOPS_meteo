#!/bin/bash


# exécuter ce fichier dans un terminal à partir de la racine du projet à l'aide des deux commandes suivantes
#-----------------------------------------------------------------------
#chmod +x ./docker/weather_db_mysql_docker/1.0-pdkengne-create-weather-db-image.sh
#./docker/weather_db_mysql_docker/1.0-pdkengne-create-weather-db-image.sh
#-----------------------------------------------------------------------


# build image
docker build -t mysql_weather_docker ./docker/weather_db_mysql_docker/


# tag the created image
docker tag mysql_weather_docker:latest march2023mlops/mysql_weather_docker:latest


# log into the Docker public registry
docker login --username march2023mlops --password march2023mlops


# push a new tag to the created image
docker push march2023mlops/mysql_weather_docker:latest


# remove the first created image
docker rmi mysql_weather_docker:latest


# Test the created image without a volume
# docker pull march2023mlops/mysql_user_docker:latest
docker run --name weatherdb -d -p 3306:3306 \
 -e MYSQL_ROOT_PASSWORD=my-secret-pw \
 march2023mlops/mysql_weather_docker:latest
  
 
# enter into the created container
#docker container start weatherdb

docker exec -it weatherdb bash


# launch mysql 
mysql -u root -p 

# type this password 
password: my-secret-pw


# show our mysql configuration
SHOW VARIABLES LIKE 'secure_file_priv';
SHOW GLOBAL VARIABLES LIKE 'local_infile';


# show available databases
SHOW DATABASES;


# use the weather databse
use weather;
SHOW TABLES;


# views all entries from the weathers table
SELECT COUNT(*) FROM weathers;

SELECT * FROM weathers WHERE location = 'MelbourneAirport' AND year = 2022 AND month = 10 AND day = 27;

SELECT * FROM weathers WHERE location = 'PerthAirport' AND year = 2023 AND month = 6 AND day = 01;

SELECT * FROM weathers WHERE location = 'Albury' AND year = 2022 AND month = 7 AND day = 20;

SELECT * FROM weathers WHERE location = 'Sydney' AND year = 2016 AND month = 12 AND day = 31;


# exit the mysql command prompt
exit;

# exit the container
exit

# stop the container
docker container stop weatherdb

# remove the container
docker container rm weatherdb
 
