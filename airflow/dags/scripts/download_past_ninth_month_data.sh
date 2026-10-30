#!/bin/bash



# month gap 
month_gap="9"

# chemin de sauvegarde 
saving_path="/home/airflow/raw-data/"


# liste des codes météos des villes australiennes concernées par notre études
city_codes=("IDCJDW2002" "IDCJDW2005" "IDCJDW2029" "IDCJDW2030" "IDCJDW2097" "IDCJDW2084" "IDCJDW2099" "IDCJDW2100" "IDCJDW2111" 
 "IDCJDW2119" "IDCJDW2124" "IDCJDW2125" "IDCJDW2139" "IDCJDW2145" "IDCJDW2146" "IDCJDW2801" "IDCJDW2802" "IDCJDW2804" "IDCJDW3005" 
 "IDCJDW3008" "IDCJDW2142" "IDCJDW3049" "IDCJDW3050" "IDCJDW3051" "IDCJDW3059" "IDCJDW3068" "IDCJDW3079" "IDCJDW3101" "IDCJDW4019" 
 "IDCJDW4024" "IDCJDW4050" "IDCJDW4128" "IDCJDW5081" "IDCJDW5041" "IDCJDW5049" "IDCJDW5072" "IDCJDW6001" "IDCJDW2143" "IDCJDW6108" 
 "IDCJDW6110" "IDCJDW6111" "IDCJDW6119" "IDCJDW6138" "IDCJDW7021" "IDCJDW7025" "IDCJDW8002" "IDCJDW8014" "IDCJDW8024" "IDCJDW8056")


# date (yyyymmm)
latest_dates=$(date --date=$month_gap'+ month ago' '+%Y%m')


# site web où les données sont disponibles
base_url="http://www.bom.gov.au/climate/dwo/"


for base_city_code in "${city_codes[@]}"
do
  # nom du fichier à télécharger
  file_name=${base_city_code}"."${latest_dates}".csv" 
  # liens complet de téléchargement du fichier   
  full_url=${base_url}${latest_dates}"/text/"${file_name} 
  # téléchargement et sauvegarde du fichier
  http GET $full_url > "${saving_path}${file_name}"          
done


# vérifier que le dernier fichier téléchargé est nom vide
head -n 6 "${saving_path}${file_name}"
echo "..."
echo "..."
tail -n 2 "${saving_path}${file_name}"

