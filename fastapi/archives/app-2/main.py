from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import date
import joblib

app = FastAPI()
security = HTTPBasic()

# Vérification des informations d'identification
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "aeroport"
    correct_password = "toto_australie"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    return credentials.username

# Chargement du modèle de prédiction
model = joblib.load("../models/final-model-pipe-xgb-2023-05-26-02-05-05.pkl")

# Endpoint pour obtenir les prédictions météorologiques
@app.get("/prediction")
def get_weather_prediction(date: date, ville: str, username: str = Depends(get_current_username)):
    # Votre logique de prédiction météorologique ici en utilisant le modèle chargé (model)
    # Assumons que la fonction predict_weather retourne une prédiction pour la date et la ville spécifiées
    prediction = predict_weather(date, ville, model)
    
    return {
        "date": date,
        "ville": ville,
        "prediction": prediction
    }
