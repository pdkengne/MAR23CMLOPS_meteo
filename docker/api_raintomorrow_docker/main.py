# Main code for an API the rain weather variable in localities of Australia

# Load of required libraries
import pandas as pd
import numpy as np
import json
import os
import uvicorn
import orjson
import typing
from enum import Enum
import datetime
from datetime import date
from io import StringIO
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Header, Depends, HTTPException, status, Path, Query, Body, Form, File, UploadFile, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from typing import Annotated, List, Optional
from pydantic import BaseModel
from joblib import dump, load
import pickle



########## data modeling section 


# get the current year
#current_year=int(date.today().strftime("%Y"))

# get the current month
#current_month=int(date.today().strftime("%m"))

# get the current day
#current_day=int(date.today().strftime("%d"))



# Models for the factors of wind direction variables
class WindDirection(str, Enum):
    DIRECTION1 = 'W'
    DIRECTION2 = 'WNW'
    DIRECTION3 = 'WSW'
    DIRECTION4 = 'NE'
    DIRECTION5 = 'NNW'
    DIRECTION6 = 'N'
    DIRECTION7 = 'NNE'
    DIRECTION8 = 'SW'
    DIRECTION9 = 'ENE'
    DIRECTION10 = 'SSE'
    DIRECTION11 = 'S'
    DIRECTION12 = 'NW'
    DIRECTION13 = 'SE'
    DIRECTION14 = 'ESE'
    DIRECTION15 = 'E'
    DIRECTION16 = 'SSW'



# Model for the names of the locality variable
class LocalityName(str, Enum):
    LOCALITY1 = 'Albury'
    LOCALITY2 = 'BadgerysCreek'
    LOCALITY3 = 'Cobar'
    LOCALITY4 = 'CoffsHarbour'
    LOCALITY5 = 'Moree'
    LOCALITY6 = 'Newcastle'
    LOCALITY7 = 'NorahHead'
    LOCALITY8 = 'NorfolkIsland'
    LOCALITY9 = 'Penrith'
    LOCALITY10 = 'Richmond'
    LOCALITY11 = 'Sydney'
    LOCALITY12 = 'SydneyAirport'
    LOCALITY13 = 'WaggaWagga'
    LOCALITY14 = 'Williamtown'
    LOCALITY15 = 'Canberra'
    LOCALITY16 = 'Wollongong'
    LOCALITY17 = 'Tuggeranong'
    LOCALITY18 = 'MountGinini'
    LOCALITY19 = 'Ballarat'
    LOCALITY20 = 'Bendigo'
    LOCALITY21 = 'Sale'
    LOCALITY22 = 'MelbourneAirport'
    LOCALITY23 = 'Melbourne'
    LOCALITY24 = 'Mildura'
    LOCALITY25 = 'Nhil'
    LOCALITY26 = 'Portland'
    LOCALITY27 = 'Watsonia'
    LOCALITY28 = 'Dartmoor'
    LOCALITY29 = 'Brisbane'
    LOCALITY30 = 'Cairns'
    LOCALITY31 = 'GoldCoast'
    LOCALITY32 = 'Townsville'
    LOCALITY33 = 'Adelaide'
    LOCALITY34 = 'MountGambier'
    LOCALITY35 = 'Nuriootpa'
    LOCALITY36 = 'Woomera'
    LOCALITY37 = 'Albany'
    LOCALITY38 = 'Witchcliffe'
    LOCALITY39 = 'PearceRAAF'
    LOCALITY40 = 'PerthAirport'
    LOCALITY41 = 'Perth'
    LOCALITY42 = 'SalmonGums'
    LOCALITY43 = 'Walpole'
    LOCALITY44 = 'Hobart'
    LOCALITY45 = 'Launceston'
    LOCALITY46 = 'AliceSprings'
    LOCALITY47 = 'Darwin'
    LOCALITY48 = 'Katherine'
    LOCALITY49 = 'Uluru'
    


# model for rain weather status
class RainStatus(str, Enum):
    STATUS1 = "No"
    STATUS2 = "Yes"




# Function to select the rain weather status
async def get_raintoday(raintoday: RainStatus = Query(RainStatus.STATUS1, description="")):
    return raintoday


# Function to select the factor of wind direction
async def get_windgustdir(windgustdir: WindDirection = Query(WindDirection.DIRECTION1, description="")):
    return windgustdir


# Function to select the factor of wind direction
async def get_winddir9am(winddir9am: WindDirection = Query(WindDirection.DIRECTION6, description="")):
    return winddir9am
    

# Function to select the factor of wind direction
async def get_winddir3pm(winddir3pm: WindDirection = Query(WindDirection.DIRECTION13, description="")):
    return winddir3pm


# Function to select the name of a locality
async def get_locality(locality: LocalityName = Query(LocalityName.LOCALITY12, description="")):
    return locality



# define the date ranges
NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=7330)
Previous_Date = datetime.datetime.today() - datetime.timedelta(days=7330)
Current_Date = datetime.datetime.today()


# Function to collect custom user input data
async def get_custom_weather_data(
                    location: str = Depends(get_locality),
                    year: int = Query(int(Current_Date.year), ge=int(Previous_Date.year), le=int(NextDay_Date.year)),
                    month: int = Query(int(Current_Date.month), ge=1, le=12),
                    day: int = Query(int(Current_Date.day), ge=1, le=31),
                    raintoday: Optional[str] = Depends(get_raintoday),
                    windgustdir: Optional[str] = Depends(get_windgustdir),
                    winddir9am: Optional[str] = Depends(get_winddir9am),
                    winddir3pm: Optional[str] = Depends(get_winddir3pm),
                    windgustspeed: Optional[float] = Query(None, ge=0, le=300),
                    windspeed9am: Optional[float] = Query(None, ge=0, le=300),
                    windspeed3pm: Optional[float] = Query(None, ge=0, le=300),
                    mintemp: Optional[float] = Query(None, ge=-100, le=100),
                    maxtemp: Optional[float] = Query(None, ge=-100, le=100),
                    temp9am: Optional[float] = Query(None, ge=-100, le=100),
                    temp3pm: Optional[float] = Query(None, ge=-100, le=100),
                    rainfall: Optional[float] = Query(None, ge=0, le=500),
                    evaporation: Optional[float] = Query(None, ge=0, le=200),
                    sunshine: Optional[float] = Query(None, ge=0, le=30),  
                    humidity9am: Optional[float] = Query(None, ge=0, le=100),
                    humidity3pm: Optional[float] = Query(None, ge=0, le=100),
                    pressure9am: Optional[float] = Query(None, ge=500, le=1500),
                    pressure3pm: Optional[float] = Query(None, ge=500, le=1500),
                    cloud9am: Optional[float] = Query(None, ge=0, le=9),
                    cloud3pm: Optional[float] = Query(None, ge=0, le=9)):   
    
    custom_weather_data = {'location': location,
                    'mintemp': mintemp,
                    'maxtemp': maxtemp,
                    'rainfall': rainfall,
                    'evaporation': evaporation,
                    'sunshine': sunshine,
                    'windgustdir': windgustdir,
                    'windgustspeed': windgustspeed,
                    'winddir9am': winddir9am,
                    'winddir3pm': winddir3pm,
                    'windspeed9am': windspeed9am,
                    'windspeed3pm': windspeed3pm,
                    'humidity9am': humidity9am,
                    'humidity3pm': humidity3pm,
                    'pressure9am': pressure9am,
                    'pressure3pm': pressure3pm,
                    'cloud9am': cloud9am,
                    'cloud3pm': cloud3pm,
                    'temp9am': temp9am,
                    'temp3pm': temp3pm,
                    'raintoday': raintoday,
                    'year': year,
                    'month': month,
                    'day': day
                    }
    
    return custom_weather_data
    



# Function to collect the user input data
async def get_weather_data(
                    location: str = Depends(get_locality),
                    year: int = Query(int(Current_Date.year), ge=int(Previous_Date.year), le=int(NextDay_Date.year)),
                    month: int = Query(int(Current_Date.month), ge=1, le=12),
                    day: int = Query(int(Current_Date.day), ge=1, le=31)):   
    
    weather_data = {'location': location,
                    'year': year,
                    'month': month,
                    'day': day
                    }
    
    return weather_data

    



########## data loading section



# change the current directory to the directory containing the running script file (main.py)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# load the saved model pipeline
# model file path
model_path ='./models/best-model-pipe.pkl'
#model = pickle.load(open(model_path, 'rb'))


# Read the CSV file: dataset of weather data
# data file path
data_path ='./weather-data/processed-weather-aus-up-to-date.csv'
#df_data = pd.read_csv(data_path)
# Replace missing values with "None"
#df_data = df_data.replace(np.nan, None)


# Opening JSON file: database of users
users_path = './user-data/users.json'
with open(users_path, 'r') as openfile:
    # Reading from json file
    users = json.load(openfile)



# Opening JSON file: dataset of model performance
# metrics file path
eval_metrics_path ='./model-evaluation/classification_report_eval.json'
#with open(eval_metrics_path, 'r') as openfile:
#    # Reading from json file
#    classification_report = json.load(openfile)


train_metrics_path ='./model-evaluation/classification_report_train.json'
#with open(train_metrics_path, 'r') as openfile:
#    # Reading from json file
#    classification_report = json.load(openfile)


train_metrics_path_bis ='./model-evaluation/classification_report_train_bis.json'
#with open(train_metrics_path_bis, 'r') as openfile:
#    # Reading from json file
#    classification_report = json.load(openfile)



########## api definition section

        

# Create an application object 
api = FastAPI(
	title = 'Australia weather forecast',
	description = "An API to predict tomorrow's rainy weather in Australia",
	version ="1.0.1",
    openapi_tags=[
    {
        'name': 'Home Page',
        'description': 'Check the status of the API, create a user account and login'
    },
    {
        'name': 'Model Predictions',
        'description': 'Compute model predictions'
    },
    {
        'name': 'Model Performance',
        'description': 'Monitor model performance'
    }
])



########## route definition section


# Implementation of the health endpoint
@api.get("/health", tags=['Home Page'], description="Returns Greetings and User-Agent")
async def get_header(name: str, user_agent: Annotated[str | None, Header()] = None):
    response = {
                'message': f'Welcome {name} to our Australia weather forecast API !',
                "user_agent": user_agent
               }
    return response



# Implementation of the registration endpoint
@api.post("/sign-up", 
        tags=['Home Page'], 
        description="Create account information to login",
        status_code=status.HTTP_201_CREATED)
async def create_account(username: Annotated[str, Form()], 
                         password: Annotated[str, Form()],
                         surname: Annotated[str, Form()] = None,
                         name: Annotated[str, Form()] = None,
                         email: Annotated[str, Form()] = None):
    if username in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username already exists"
        )      
    users[username] = {
        "username":  username,
        "hashed_password": pwd_context.hash(password),
        "surname": surname,
        "name": name,
        "email": email
        }
    # Serializing json
    json_object = json.dumps(users, indent=4)
    # Writing to users.json
    with open(users_path, "w") as outfile:
        outfile.write(json_object)
    response = {"message": "User successfully registered!"}
    return response
    
    

# Implementation of a simple HTTP Basic Authentication
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



# Implementation of the login endpoint
@api.get("/sign-in", tags=['Home Page'], description="Enter the login credentials")
async def get_access(username: str = Depends(get_current_user)):
    response = {"message": f"Hello {username}!"}
    return response
    
    

# Implementation of the endpoint to retrieve all registered users. The access is restricted to an administrator
@api.get("/users/retrieve", 
        tags=['Home Page'], 
        dependencies=[Depends(get_current_user)],
        description="Retrieve all user accounts from the users database. The access is restricted to an administrator.")
async def retrieve_all_users(username: str = Depends(get_current_user)):
    # Restrict access to an administrator
    if username == "admin":
        return users
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials passed")



# Implementation of the endpoint to perform a forecast.
@api.get("/next-day-rain/forecast/ordinary", 
        tags=['Model Predictions'], 
        dependencies=[Depends(get_current_user), Depends(get_weather_data)],
        description="""
        Compute the next day rain forecast associated with the specified date and location provided by the user.
        
        Here, the model is trained on a dataset which consists of weather data associated with the last 3660 days before the current day.
        """)
async def make_ordinary_prediction(weather: dict = Depends(get_weather_data), username: str = Depends(get_current_user)):
    # check if the model and data file paths exist 
    if os.path.exists(data_path) and os.path.exists(model_path):
        # Read the CSV file: dataset of weather data
        df_data = pd.read_csv(data_path)
        # Replace missing values with "None"
        df_data = df_data.replace(np.nan, None)
        selected_weather_df = df_data[(df_data["location"] == weather["location"])&(df_data["year"] == weather["year"])&(df_data["month"] == weather["month"])&(df_data["day"] == weather["day"])]
        selected_weather_df["windgustdir"].fillna(value="W", inplace=True)
        selected_weather_df["winddir9am"].fillna(value="N", inplace=True)
        selected_weather_df["winddir3pm"].fillna(value="SE", inplace=True)
        if int(selected_weather_df.size) != 0:
            # load the saved model pipeline
            model = pickle.load(open(model_path, 'rb'))
            selected_weather_df["predicted_raintomorrow"] = int(model.predict(selected_weather_df))
            selected_weather_df["predicted_raintomorrow"].replace({0:"No", 1:"Yes"}, inplace = True)
            response = selected_weather_df.to_dict()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, the internal database doesn't contain weather data associated with supplied date.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, the server is busy. The machine learning model or the weather database is inaccessible. Please try again later.")
    return response



# Implementation of the endpoint to perform a custom forecast.
@api.get("/next-day-rain/forecast/custom", 
        tags=['Model Predictions'], 
        dependencies=[Depends(get_current_user), Depends(get_custom_weather_data)],
        description="""
        Compute the next day rain forecast associated with the specified date and location along with a custom weather data provided by the user.
        
        Here, the model is trained on a dataset which consists of weather data associated with the last 3660 days before the current day.
        """)
async def make_custom_prediction(weather: dict = Depends(get_custom_weather_data), username: str = Depends(get_current_user)):
    # check if the model file path exists
    if os.path.exists(model_path):
        # load the saved model pipeline
        model = pickle.load(open(model_path, 'rb'))
        # convert input weather data dictionary to a data frame
        weather_df=pd.DataFrame.from_dict(weather, orient = "index").transpose()
        weather_df["predicted_raintomorrow"] = int(model.predict(weather_df))
        weather_df["predicted_raintomorrow"].replace({0:"No", 1:"Yes"}, inplace = True)
        response = weather_df.to_dict()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, the server is busy. The machine learning model is inaccessible. Please try again later.")
    return response





# Implementation of the endpoint to diplay the model performance numerical info.
@api.get("/model/evaluation", 
        tags=['Model Performance'], 
        dependencies=[Depends(get_current_user)],
        description="""
        Diplay the model performance numerical info. 
        
        Here, the model is evaluated on a test dataset which consists of weather data associated with the last 366 days before the current day.
        """)
async def dipslay_test_metrics():
    # check if the metrics file path exists
    if os.path.exists(eval_metrics_path):
        # Opening JSON file: dataset of model performance
        with open(eval_metrics_path, 'r') as openfile:
            # Reading from json file
            classification_report = json.load(openfile)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, the server is busy. The machine learning model performance report is inaccessible. Please try again later.")
    return classification_report 




# Implementation of the endpoint to diplay the model performance numerical info.
@api.get("/model/estimation-1", 
        tags=['Model Performance'], 
        dependencies=[Depends(get_current_user)],
        description="""
        Diplay the model performance numerical info. 
        
        Here, the model is evaluated on a training dataset which consists of weather data associated with the last 3660 days before the 366-th days from the current day.
        """)
async def dipslay_train_metrics():
    # check if the metrics file path exists
    if os.path.exists(train_metrics_path_bis):
        # Opening JSON file: dataset of model performance
        with open(train_metrics_path_bis, 'r') as openfile:
            # Reading from json file
            classification_report = json.load(openfile)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, the server is busy. The machine learning model performance report is inaccessible. Please try again later.")
    return classification_report




# Implementation of the endpoint to diplay the model performance numerical info.
@api.get("/model/estimation-2", 
        tags=['Model Performance'], 
        dependencies=[Depends(get_current_user)],
        description="""
        Diplay the model performance numerical info. 
        
        Here, the model is evaluated on a training dataset which consists of weather data associated with the last 3660 days before the current day.
        """)
async def dipslay_train_metrics():
    # check if the metrics file path exists
    if os.path.exists(train_metrics_path):
        # Opening JSON file: dataset of model performance
        with open(train_metrics_path, 'r') as openfile:
            # Reading from json file
            classification_report = json.load(openfile)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sorry, the server is busy. The machine learning model performance report is inaccessible. Please try again later.")
    return classification_report

    
    
