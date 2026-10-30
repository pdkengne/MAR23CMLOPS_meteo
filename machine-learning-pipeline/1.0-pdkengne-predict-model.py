# exploitation du meilleur modèle sauvegardé

# chargement de quelques modules d'analyse de données
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# chargement de quelques modules de machine learning
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score,recall_score
from sklearn.model_selection import cross_val_score
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder
from sklearn.compose import make_column_transformer, ColumnTransformer
from imblearn.over_sampling import SMOTE
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
    
    # extract dataset of the feature variables
    features = df.drop(['raintomorrow'], axis=1, inplace=False)
    
    # extract the datset of the target variable
    target = df['raintomorrow']
    
    # transform the target data to numerical data
    target.replace({'No':0, 'Yes': 1}, inplace = True)
    
    return features, target


# function to load the saved estimated machine learning pipeline
def load_saved_estimated_ml_model_pipeline(input_path):
    # load the saved model pipeline
    pickled_model = pickle.load(open(input_path, 'rb'))
    return pickled_model


# function to compute, plot and save the confusion matrix
def compute_and_save_confusion_matrix_plot(y_true, y_pred, ouput_path):
    confusion = confusion_matrix(y_true = y_true, y_pred = y_pred)
    plot_confusion_matrix(confusion, class_names=["No","Yes"], cmap='YlOrRd')
    plt.title('confusion matrix')
    plt.savefig(ouput_path)


# function to compute and save the classification report
def compute_and_save_classification_report_csv(y_true, y_pred, ouput_path):
    report = classification_report(y_true = y_true, y_pred = y_pred, target_names = ["No","Yes"], output_dict = True)
    report_df = pd.DataFrame(report)
    report_df.to_csv(ouput_path,  sep=',', float_format='%.5f')
    print(report_df)



# function to compute and save the classification report
def compute_and_save_classification_report(y_true, y_pred, ouput_path):
    report = classification_report(y_true = y_true, y_pred = y_pred, target_names = ["No","Yes"], output_dict = True)
    # Serializing json
    json_object = json.dumps(report, indent=4)
    # Writing to sample.json
    with open(ouput_path, "w") as outfile:
        outfile.write(json_object)
    print(report)




# execution du pipeline de prédiction et d'évaluation
def run_deployed_ml_model_pipeline():
    # chemin du fichier csv à exploiter
    input_test_data_path = "./datasets/processed/latest/processed-weather-aus-latest.csv"
    
    # chemin de sauvegarde du meilleur modèle sauvegardé
    input_best_model_path = './models/best-model-pipe-2023-07-04-10-13-23.pkl'
    
    # chemin de sauvegarde de la matrice de confusion
    output_confusion_matrix_path = './models/confusion_matrix.png'
    
    # chemin de sauvegarde du rapport de classification
    output_classification_report_path = './models/classification_report.csv'
    
    # lecture des données à modéliser
    X_test, y_test = read_and_prepare_data(input_path = input_test_data_path)
    
    # chargement et utilisation du modèle sauvegardé
    pickled_best_model = load_saved_estimated_ml_model_pipeline(input_path = input_best_model_path)
    
    # utilisation du modèle chargé
    predictions = pickled_best_model.predict(X_test)
    
    # save the classification report
    compute_and_save_classification_report(y_true = y_test, y_pred = predictions, ouput_path = output_classification_report_path)
    
    # save the confusion matrix
    compute_and_save_confusion_matrix_plot(y_true = y_test, y_pred = predictions, ouput_path = output_confusion_matrix_path)


# run all
if __name__ == '__main__':
    run_deployed_ml_model_pipeline()
