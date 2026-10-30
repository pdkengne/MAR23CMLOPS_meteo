# install all the required packages
docker-compose up airflow-init

# launch in detach mode
docker-compose up -d


# airflow link: http://localhost:8080/

# api link: http://localhost:8000/docs


# shutting down previous containers
docker-compose down


# Cleaning-up the environment
docker compose down --volumes --remove-orphans
