# pipeline pour l'estimation et la sélection d'un modèle de machine learning



# chargement de quelques modules d'analyse de données
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# chargement de quelques modules de machine learning
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score,recall_score
from sklearn.model_selection import cross_val_score
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder
from sklearn.compose import make_column_transformer, ColumnTransformer
from mlxtend.plotting import plot_confusion_matrix
from joblib import dump, load
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.svm import SVC



# liste des variables explicatives numériques
num_cols = ['mintemp', 'maxtemp', 'rainfall', 'evaporation', 'sunshine', 'windgustspeed', 'windspeed9am', 'windspeed3pm', 'humidity9am',
    'humidity3pm', 'pressure9am', 'pressure3pm', 'cloud9am', 'cloud3pm', 'temp9am', 'temp3pm', 'year', 'month', 'day']



# liste des variables explicatives catégorielles
cat_cols = ['location', 'windgustdir', 'winddir9am', 'winddir3pm', 'raintoday']



# liste de toutes les variables explicatives
predictor_cols = ['location', 'mintemp', 'maxtemp', 'rainfall', 'evaporation', 'sunshine', 'windgustdir', 'windgustspeed', 
    'winddir9am', 'winddir3pm', 'windspeed9am', 'windspeed3pm', 'humidity9am', 'humidity3pm', 'pressure9am', 'pressure3pm', 
    'cloud9am', 'cloud3pm', 'temp9am', 'temp3pm', 'raintoday', 'year', 'month', 'day']



# nom de la variable réponse
response_col = 'raintomorrow'



# function to read and return the datasets of features and target
def read_and_prepare_data(input_path):
    # read the dataset
    df = pd.read_csv(input_path)
    
    # remove missing values from the response variable (raintomorrow)
    df.dropna(subset=['raintomorrow'], inplace = True) 
        
    # extract dataset of the feature variables
    features = df.drop(['raintomorrow'], axis=1, inplace=False)
        
    # extract the datset of the target variable
    target = df['raintomorrow']
    
    # transform the target data to numerical data
    target.replace({'No':0, 'Yes': 1}, inplace = True)
    
    return features, target



# function to build the full machine learning pipeline
def build_full_ml_pipeline(
    ml_estimator,
    num_vars = num_cols, 
    cat_vars = cat_cols,
    impute_num = SimpleImputer(strategy="median"), 
    impute_var = SimpleImputer(strategy="most_frequent"), 
    scaler_num = StandardScaler(),
    encoder_cat = OneHotEncoder()):
        # pipeline to transform numerical variables
        numeric_transformer = make_pipeline((impute_num), (scaler_num)) 
        
        # pipeline to transform categorical variables
        categorical_transformer = make_pipeline((impute_var), (encoder_cat))
        
        # combination of feature transformation pipelines
        preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, num_vars), ('cat', categorical_transformer, cat_vars)])
        
        # incorporat the machine learning estimator to the pipeline
        model = Pipeline(steps=[('preprocessing', preprocessor), ('regressor', ml_estimator)])
    
        return model



# function to compute a machine learning classifier accuracy score
def compute_accuracy_score(estimator, X, y):
    # create the full model pipeline
    pipe_model = build_full_ml_pipeline(ml_estimator = estimator)
    
    # create training and test datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y, test_size = 0.3, random_state=57)
    
    # estimte the provided model pipeline on the training datasets
    pipe_model.fit(X_train, y_train)
    
    # evaluate the estimated model on the test datasets
    predictions = pipe_model.predict(X_test)
    model_score = accuracy_score(y_test, predictions)
    
    return model_score



# function to estimate and save the full machine learning pipeline
def estimate_and_save_ml_model_pipeline(estimator, X, y, output_path):
    # create the full model pipeline
    pipe_model = build_full_ml_pipeline(ml_estimator = estimator)
    
    # estimte the provided model pipeline
    pipe_model.fit(X, y)
    
    # save the estimated model pipeline
    pickle.dump(pipe_model, open(output_path, 'wb'))
    #dump(pipe_model, output_path)
    
    # print the saved model path
    print(str(pipe_model), 'saved at ', output_path)



# function to load the saved estimated machine learning pipeline
def load_saved_estimated_ml_model_pipeline(input_path):
    # load the saved model pipeline
    pickled_model = pickle.load(open(input_path, 'rb'))
    #pickled_model = load(input_path)
    return pickled_model



# function to compute and save the classification report
def compute_and_save_classification_report(y_true, y_pred, ouput_path):
    report = classification_report(y_true = y_true, y_pred = y_pred, target_names = ["No","Yes"], output_dict = True)
    # Serializing json
    json_object = json.dumps(report, indent=4)
    # Writing to sample.json
    with open(ouput_path, "w") as outfile:
        outfile.write(json_object)
    print(report)

