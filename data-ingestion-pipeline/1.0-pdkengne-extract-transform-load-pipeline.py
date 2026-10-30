# pipeline pour les opérations ETL


# chargement des librairies
import glob as g
import pandas as pd
import numpy as np
from datetime import datetime
import os


# dictionnaire pour changer les codes des localités en noms des localités
location_mapper = {
    "IDCJDW2002": "Albury",
    "IDCJDW2005": "BadgerysCreek",
    "IDCJDW2029": "Cobar",
    "IDCJDW2097": "Newcastle", 
    "IDCJDW2030": "CoffsHarbour",
    "IDCJDW2084": "Moree",
    "IDCJDW2099": "NorahHead",
    "IDCJDW2100": "NorfolkIsland",
    "IDCJDW2111": "Penrith",
    "IDCJDW2119": "Richmond",
    "IDCJDW2124": "Sydney",
    "IDCJDW2125": "SydneyAirport",
    "IDCJDW2139": "WaggaWagga",
    "IDCJDW2145": "Williamtown", 
    "IDCJDW2146": "Wollongong",
    "IDCJDW2801": "Canberra",
    "IDCJDW2802": "Tuggeranong",
    "IDCJDW2804": "MountGinini",
    "IDCJDW3005": "Ballarat",
    "IDCJDW3008": "Bendigo",
    "IDCJDW2142": "Sale",
    "IDCJDW3049": "MelbourneAirport",
    "IDCJDW3050": "Melbourne",
    "IDCJDW3051": "Mildura", 
    "IDCJDW3059": "Nhil",
    "IDCJDW3068": "Portland",
    "IDCJDW3079": "Watsonia",
    "IDCJDW3101": "Dartmoor",
    "IDCJDW4019": "Brisbane",
    "IDCJDW4024": "Cairns",
    "IDCJDW4050": "GoldCoast",
    "IDCJDW4128": "Townsville",
    "IDCJDW5081": "Adelaide",
    "IDCJDW5041": "MountGambier", 
    "IDCJDW5049": "Nuriootpa",
    "IDCJDW5072": "Woomera",
    "IDCJDW6001": "Albany",
    "IDCJDW2143": "Witchcliffe",
    "IDCJDW6108": "PearceRAAF",
    "IDCJDW6110": "PerthAirport",
    "IDCJDW6111": "Perth",
    "IDCJDW6119": "SalmonGums",
    "IDCJDW6138": "Walpole",
    "IDCJDW7021": "Hobart", 
    "IDCJDW7025": "Launceston",
    "IDCJDW8002": "AliceSprings",
    "IDCJDW8014": "Darwin",
    "IDCJDW8024": "Katherine",
    "IDCJDW8056": "Uluru"
    }


# dictionnaire pour renommer l'ensemble des colonnes
columns_mapper = {
    "Minimum temperature (°C)": "mintemp",
    "Maximum temperature (°C)": "maxtemp",
    "Rainfall (mm)": "rainfall",
    "Evaporation (mm)": "evaporation",
    "Sunshine (hours)": "sunshine",
    "Direction of maximum wind gust ": "windgustdir",
    "Speed of maximum wind gust (km/h)": "windgustspeed",
    "9am Temperature (°C)": "temp9am",
    "9am relative humidity (%)": "humidity9am",
    "9am cloud amount (oktas)": "cloud9am",
    "9am wind direction": "winddir9am",
    "9am wind speed (km/h)": "windspeed9am",
    "9am MSL pressure (hPa)": "pressure9am",
    "3pm Temperature (°C)": "temp3pm",
    "3pm relative humidity (%)": "humidity3pm",
    "3pm cloud amount (oktas)": "cloud3pm",
    "3pm wind direction": "winddir3pm",
    "3pm wind speed (km/h)": "windspeed3pm",
    "3pm MSL pressure (hPa)": "pressure3pm",
    "Year": "year",
    "Month": "month",
    "Day": "day",
    "Location": "location",
    "RainToday": "raintoday",
    "RainTomorrow": "raintomorrow"                  
    }


# noms des colonnes (dans le bon ordre) à associer au fichier final
columns_order = [
    "location","mintemp","maxtemp","rainfall","evaporation","sunshine","windgustdir","windgustspeed",
    "winddir9am","winddir3pm","windspeed9am","windspeed3pm","humidity9am","humidity3pm","pressure9am",
    "pressure3pm","cloud9am","cloud3pm","temp9am","temp3pm","raintoday","raintomorrow","year","month","day"
    ]


# noms des colonnes dans les fichiers cvs à manipuler
csv_col_names=[
    'Location', 'Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)',
    'Rainfall (mm)', 'Evaporation (mm)', 'Sunshine (hours)',
    'Direction of maximum wind gust ', 'Speed of maximum wind gust (km/h)',
    'Time of maximum wind gust', '9am Temperature (°C)',
    '9am relative humidity (%)', '9am cloud amount (oktas)',
    '9am wind direction', '9am wind speed (km/h)', '9am MSL pressure (hPa)',
    '3pm Temperature (°C)', '3pm relative humidity (%)',
    '3pm cloud amount (oktas)', '3pm wind direction',
    '3pm wind speed (km/h)', '3pm MSL pressure (hPa)'
    ]


# colonnes des variables numériques
num_cols = [
    'Minimum temperature (°C)', 'Maximum temperature (°C)', 'Rainfall (mm)', 'Evaporation (mm)', 'Sunshine (hours)',
    'Speed of maximum wind gust (km/h)', '9am Temperature (°C)', '9am relative humidity (%)', '9am cloud amount (oktas)',
    '9am MSL pressure (hPa)', '9am wind speed (km/h)', '3pm Temperature (°C)', '3pm relative humidity (%)', '3pm cloud amount (oktas)',
    '3pm wind speed (km/h)', '3pm MSL pressure (hPa)'
    ]



# extraction for old data
def extract_old(path):
    # chargement du dataset
    extracted_data = pd.read_csv(path)
    return extracted_data
    


# transformation for old data
def transform_old(data):
    # conversion de la colonne Date en un object de type datetime
    data['Date'] = pd.to_datetime(data['Date'])
    # création de nouvelles colonnes reliées à la date
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    # suppression des lignes dont toutes les valeurs sont nulles à l'exception des valeurs Date et Location
    data.dropna(axis = 0, thresh = 3, inplace = True)
    # suppression de la colonne Date
    data.drop('Date', axis = 1, inplace=True)
    # suppression de la colone RISK_MM
    data.drop(["RISK_MM"], axis=1, inplace=True)
    # transformation des noms de colonne en miniscule
    data.columns = data.columns.str.lower()
    # suppression des lignes ayant des valeurs manquantes dans la variable réponse (raintomorrow)
    data.dropna(subset=['raintomorrow'], inplace = True)
          
    return data
    


# extraction
def extract(folder):
    extracted_data = pd.DataFrame(columns = csv_col_names)
    
    for file in g.glob(folder):
        df = pd.read_csv(file, encoding = "ISO-8859-1", names = csv_col_names)
        text = df["Location"][1]
        code = text.split(".")[0].split(" ")[-1]
        df["Location"] = code
        
        df.dropna(thresh=3, axis=0, inplace=True)
        df.drop(index=df.index[0], axis=0, inplace=True)
        
        df['9am wind speed (km/h)'].replace({"Calm": 1}, inplace = True)
        df['3pm wind speed (km/h)'].replace({"Calm": 1}, inplace = True)
        
        df[num_cols] = df[num_cols].astype(float, errors='raise')
        
        extracted_data = pd.concat([extracted_data, df], ignore_index = True)
        extracted_data["Location"].replace(location_mapper, inplace = True)
        
    return extracted_data



# Transformation
def transform(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    
    data.drop("Time of maximum wind gust", axis = 1, inplace=True)

    data["RainToday"] = data["Rainfall (mm)"] >= 1
    data["RainToday"].replace({False:"No", True: "Yes"}, inplace = True)

    res = pd.DataFrame(columns = data.columns)
    localities = data["Location"].unique()
    for city in localities:
        df = data[data["Location"] == city].copy()
        df.set_index('Date', inplace=True)
        df.sort_index(axis=0, level=None, ascending=True, inplace=True)
        df["RainTomorrow"] = df.shift(-1)["RainToday"]
        res = pd.concat([res, df], axis=0, ignore_index = True)

    res.rename(columns=columns_mapper, inplace=True)
    res = res.reindex(columns=columns_order, copy=True)
    
    return res


# chargement
def load(target_file, data_to_load):
    data_to_load.to_csv(target_file, index = False)



# selection des données jusqu'à une certaine profondeur (en jours) dans le passé
# à partir d'une date passée exprimée en nombre de jour par rapport au présent
def select_data_ndays_ago(data, ndays = 0, start = 0):
    start_date = datetime.today() - timedelta(days = start)
 
    res = pd.DataFrame(columns = data.columns)
    
    for d in range(0, ndays + 1):
        previous_date = start_date - timedelta(days = d)
        day = previous_date.day
        month = previous_date.month
        year = previous_date.year

        df = data[(data.year== year)&(data.month==month)&(data.day==day)]
        res = pd.concat([res, df], axis=0, ignore_index = True)

    return res



# générer un rapport d'analyse exploratoire
def generate_eda_report(data, title, output_file):
    profile = ProfileReport(data, title = title, html = {'style':{'full_width':True}})
    profile.to_file(output_file = output_file)



# execution du pipeline ETL
def run_etl():
    # dossier des fichiers csv à manipuler
    input_path = "./datasets/raw/latest/*.csv"
    
    # chemin du fichier csv des données anciennes (15 ans vers le passé)
    input_path_old = "./datasets/raw/dec2008-march2023/weatherAUS-2.csv"
    
    # chemin de sauvegarde du fichier final
    output_path = './datasets/processed/latest/processed-weather-aus-latest.csv'
    
    # chemin de sauvegarde des données complètes à jour
    save_path = './datasets/processed/up-to-date/processed-weather-aus-up-to-date.csv'
    
    # chargement des données anciennes (1 an vers le passé)
    df = pd.read_csv('./datasets/processed/may2022-may2023/processed-weather-aus-may2022-may2023.csv')
    
    
    # chargement des données récentes
    extracted_data = extract(folder = input_path)
    
    # transformation des données récentes
    transformed_data = transform(data = extracted_data)
    
    # sauvegarde des données récentes transformées
    loaded_data = load(target_file = output_path, data_to_load = transformed_data)
    
    
    # chargement des données anciennes (15 ans vers le passé)
    extracted_data_old = extract_old(path = input_path_old)
    
    # transformation des données anciennes (15 ans vers le passé)
    transformed_data_old = transform_old(data = extracted_data_old)
    
    
        
    # fusion des données anciennes et récentes
    df_merged = pd.concat([transformed_data_old, df, transformed_data], ignore_index = True).drop_duplicates()
    
    # sauvegarde des données complètes à jour
    loaded_data = load(target_file = save_path, data_to_load = df_merged)


# run all
if __name__ == '__main__':
    run_etl()
