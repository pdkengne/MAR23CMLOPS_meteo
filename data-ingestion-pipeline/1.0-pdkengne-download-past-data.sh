#!/bin/bash


# exécuter ce fichier dans un terminal à partir de la racine du projet à l'aide des deux commandes suivantes
#-----------------------------------------------------------------------
#chmod +x ./data-ingestion-pipeline/1.0-pdkengne-download-past-data.sh
#./data-ingestion-pipeline/1.0-pdkengne-download-past-data.sh
#-----------------------------------------------------------------------


# liste des codes météos des villes australiennes concernées par notre études
city_codes=("IDCJDW2002" "IDCJDW2005" "IDCJDW2029" "IDCJDW2030" "IDCJDW2097" "IDCJDW2084" "IDCJDW2099" "IDCJDW2100" "IDCJDW2111" 
 "IDCJDW2119" "IDCJDW2124" "IDCJDW2125" "IDCJDW2139" "IDCJDW2145" "IDCJDW2146" "IDCJDW2801" "IDCJDW2802" "IDCJDW2804" "IDCJDW3005" 
 "IDCJDW3008" "IDCJDW2142" "IDCJDW3049" "IDCJDW3050" "IDCJDW3051" "IDCJDW3059" "IDCJDW3068" "IDCJDW3079" "IDCJDW3101" "IDCJDW4019" 
 "IDCJDW4024" "IDCJDW4050" "IDCJDW4128" "IDCJDW5081" "IDCJDW5041" "IDCJDW5049" "IDCJDW5072" "IDCJDW6001" "IDCJDW2143" "IDCJDW6108" 
 "IDCJDW6110" "IDCJDW6111" "IDCJDW6119" "IDCJDW6138" "IDCJDW7021" "IDCJDW7025" "IDCJDW8002" "IDCJDW8014" "IDCJDW8024" "IDCJDW8056")


# liste des dates passées où les données sont encore disponibles en téléchargement (il s'agit des 13 derniers mois + le mois en cours)
past_dates=("202205" "202206" "202207" "202208" "202209" "202210" "202211" "202212" "202301" "202302" "202303" "202304" "202305")


# site web où les données sont disponibles
base_url="http://www.bom.gov.au/climate/dwo/"


# chemin de sauvegarde des données 
saving_path="./datasets/raw/may2022-may2023/"


for base_city_code in "${city_codes[@]}"
do
  for base_date in "${past_dates[@]}"
  do
    # nom du fichier à télécharger
    file_name=${base_city_code}"."${base_date}".csv" 
    # liens complet de téléchargement du fichier   
    full_url=${base_url}${base_date}"/text/"${file_name} 
    # téléchargement et sauvegarde du fichier
    http GET $full_url > ${saving_path}${file_name}       
  done    
done
