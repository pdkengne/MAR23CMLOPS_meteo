#!/bin/bash


# exécuter ce fichier dans un terminal à partir de la racine du projet à l'aide des deux commandes suivantes
#-----------------------------------------------------------------------
#chmod +x ./src/databases/user_db_mysql_docker/1.0-pdkengne-create-user-db-image.sh
#./src/databases/user_db_mysql_docker/1.0-pdkengne-create-user-db-image.sh
#-----------------------------------------------------------------------


# build image
docker build -t mysql_user_docker ./src/databases/user_db_mysql_docker/


# tag the created image
docker tag mysql_user_docker:latest march2023mlops/mysql_user_docker:latest


# log into the Docker public registry
docker login --username march2023mlops --password march2023mlops


# push a new tag to the created image
docker push march2023mlops/mysql_user_docker:latest


# remove the first created image
docker rmi mysql_user_docker:latest


# Test the created image with a volume
#docker pull march2023mlops/mysql_user_docker:latest
docker run --name userdb -d -p 3306:3306 \
 -e MYSQL_ROOT_PASSWORD=my-secret-pw \
 -v ./src/databases/user_db_mysql_docker/userdb_volume:/var/lib/mysql \
 march2023mlops/mysql_user_docker:latest



# Test the created image without a volume
# docker pull march2023mlops/mysql_user_docker:latest
#docker run --name userdb -d -p 3306:3306 \
# -e MYSQL_ROOT_PASSWORD=my-secret-pw \
# march2023mlops/mysql_user_docker:latest


# enter into the created container
docker exec -it userdb bash

# launch mysql 
mysql -u root -p 

# type this password 
password: my-secret-pw

# use the user databse
use user;

# inser a new entry in the users table
INSERT INTO users(first_name, last_name, email, username, password, role)
 VALUES
     ('daniel', 'help', 'daniel.help@datascientest.com', 'hdaniel', 'hdaniel', 'standard');

# views all entries from the users table
SELECT * FROM users;

# exit the mysql command prompt
exit;

# exit the container
exit

# stop the container
docker container stop userdb

# remove the container
docker container rm userdb



