#### Importation Package

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import List, Optional

import pandas as pd
from random import sample
import json

from pydantic import BaseModel

### variable
path = '/home/ubuntu/MAR23CMLOPS_meteo/'
path_data = path + 'data/processed/'
path_api = path + 'src/app/'
path_user = path + 'src/data/'

#### importation données

# Fichier du modele
df_data = pd.read_csv(path_data+'processed-data-2023-05-25-22-21-11.csv')

# Fichier des utilisateurs
df_user = pd.read_csv(path_user+'user.csv')

#### Instanciation 

api = FastAPI(
	title = 'API Projet Meteo',
	description = "L'objectif de cette API est de récupérer les résultats du modèle de ",
	version ="0.0.1"
	)
security = HTTPBasic()

#### Déclaration fonction et Objet

def dic_user(df):
	users = {}
	for i in range(len(df_user)):
		users[df_user.iloc[i,0]] = df_user.iloc[i,1]
	return users

def security_http(credentials:HTTPBasicCredentials = Depends(security)):
	""" Gestion de la sécurité a partir de la base utilisateur
	"""
	username = credentials.username
	password = credentials.password
	if username in users.keys() and password in users.values():
		return {"username":credentials.username, "password": credentials.password}
	raise HTTPException(status_code=401,
				detail="Identifiants non reconnus",
				headers={"WWW-Authenticate":"Basic"})
#def security_token(...):
	""" Gestion de la sécurité a partir de token - A construire
	"""

class User(BaseModel):
	""" Modèle d'info utilisateur
	"""
	Nom: str
	Prenom: str
	login: str
	password: str
	role: str

class airport(BaseModel):
	"""  Mapping ville-aéroport
	"""
	aeroport_id: str
	aeroport_name: str
	town: str
#### Initialisation liste
users = dic_user(df_user)	
#### Endpoint

@api.get('/forecast')
def get_forecast(location: str, year: int, month: int, day: int, credentials:HTTPBasicCredentials = Depends(security_http)):
	fct = df_data[(df_data.location==location)&(df_data.year== year)&(df_data.month==month)&(df_data.day==day)]
	if fct.iloc[0,21]=='Yes':
		ans = 'Il va pleuvoir demain sur '+fct.iloc[0,0]
	else: 
		ans = 'Il ne va pas pleuvoir demain sur '+fct.iloc[0,0]
	return {'message':ans}
#	return {'message':fct.iloc[0,0]}
@api.get('/test', name="test de l'API" )
def test_api():
	return {'message':"l'API est en marche"}

@api.get('/user',name="Vérification de la liste de user")
def get_user(credentials:HTTPBasicCredentials = Depends(security)):
	""" ce endpoint n'est accessible qu'au profil admin
	"""
	if credentials.username=='admin' and credentials.password=='admin':
		return users

@api.put('/add_users', name = "ajout d'un user")
def post_user(user: User, credentials:HTTPBasicCredentials = Depends(security)):
	""" ce endpoint n'est accessible qu'au profil admin
	"""
	if credentials.username=='admin' and credentials.password=='admin':
		global df_user
		add_user = {
			"Nom": user.Nom,
			"Prenom": user.Prenom,
			"username":user.login,
			"password":user.password,
			"role":user.role
		}
		df_user = pd.concat([df_user, pd.DataFrame([add_user])],axis=0).drop_duplicates()
		df_user.to_csv(path_user+'user.csv', index=False)
		return {'message' : 'le user '+add_user["username"]+" a été ajouté"}
	else:
		return {'message' : 'action non autorisé'}
