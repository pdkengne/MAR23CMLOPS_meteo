#!/bin/bash


# chemin de sauvegarde des données 
saving_path="/home/airflow/raw-historical-data/weatherAUS-2.csv"

# téléchargement et sauvegarde des données
http GET "https://rattle.togaware.com/weatherAUS.csv" > "${saving_path}"

# vérifier que le fichier téléchargé est nom vide
head -n 2 "${saving_path}"
echo "..."
echo "..."
tail -n 2 "${saving_path}"
