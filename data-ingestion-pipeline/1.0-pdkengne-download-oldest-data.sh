#!/bin/bash


# exécuter ce fichier dans un terminal à partir de la racine du projet à l'aide des deux commandes suivantes
#-----------------------------------------------------------------------
#chmod +x ./data-ingestion-pipeline/1.0-pdkengne-download-oldest-data.sh
#./data-ingestion-pipeline/1.0-pdkengne-download-oldest-data.sh
#-----------------------------------------------------------------------


http GET "https://rattle.togaware.com/weatherAUS.csv" > ./datasets/raw/dec2008-march2023/weatherAUS-2.csv


