#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

import dataops
import modelsops
import os
import json
import numpy as np
import pandas as pd
from airflow import DAG
import airflow.utils.dates
from airflow.models import Variable
from datetime import datetime, timedelta, date
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator


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

from ydata_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns



#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------




def transform_ongoing_and_previous_month_data():
    input_folder = '/home/airflow/raw-data/*.csv'
    path_to_output_data = '/home/airflow/processed-data/processed-data.csv'

    extracted_data = dataops.extract(input_folder)
    transformed_data = dataops.transform(data = extracted_data)
    loaded_data = dataops.load(target_file = path_to_output_data, data_to_load = transformed_data)
    print('\n', transformed_data.head(10))



def update_weather_database():
    first_path_to_input_data = '/home/airflow/processed-historical-data/processed-historical-data.csv'
    second_path_to_input_data = '/home/airflow/processed-data/processed-data.csv'
    path_to_output_data = '/home/airflow/complete-processed-dataset/processed-weather-aus-up-to-date.csv'

    historical_df = pd.read_csv(first_path_to_input_data)
    current_df = pd.read_csv(second_path_to_input_data)
    complete_df = pd.concat([historical_df, current_df], axis=0, ignore_index = True).drop_duplicates()
    
    loaded_data = dataops.load(target_file = path_to_output_data, data_to_load = complete_df)
    print('\n', complete_df.head(10))



def transform_historical_data():
    path_to_input_data = '/home/airflow/raw-historical-data/weatherAUS-2.csv'
    path_to_output_data = '/home/airflow/processed-historical-data/processed-historical-data.csv'
 
    extracted_data_old = dataops.extract_old(path = path_to_input_data)
    transformed_data_old = dataops.transform_old(data = extracted_data_old)
    loaded_data = dataops.load(target_file = path_to_output_data, data_to_load = transformed_data_old)
    print('\n', transformed_data_old.head(10))



def transform_last_fourteen_month_data():
    input_folder = '/home/airflow/raw-data/*.csv'
    path_to_output_data = '/home/airflow/processed-data/processed-data.csv'

    extracted_data = dataops.extract(input_folder)
    transformed_data = dataops.transform(data = extracted_data)
    loaded_data = dataops.load(target_file = path_to_output_data, data_to_load = transformed_data)
    print('\n', transformed_data.head(10))
     


def merge_historical_with_last_fourteen_month_data():
    first_path_to_input_data = '/home/airflow/processed-historical-data/processed-historical-data.csv'
    second_path_to_input_data = '/home/airflow/processed-data/processed-data.csv'
    path_to_output_data = '/home/airflow/complete-processed-dataset/processed-weather-aus-up-to-date.csv'

    historical_df = pd.read_csv(first_path_to_input_data)
    current_df = pd.read_csv(second_path_to_input_data)
    complete_df = pd.concat([historical_df, current_df], axis=0, ignore_index = True).drop_duplicates()
    
    loaded_data = dataops.load(target_file = path_to_output_data, data_to_load = complete_df)
    print('\n', complete_df.head(10))
   


def extract_train_data():
    path_to_input_data = '/home/airflow/complete-processed-dataset/processed-weather-aus-up-to-date.csv'
    path_to_output_data = '/home/airflow/train-data/train-data.csv'
    path_to_output_data_bis = '/home/airflow/train-data/train-data-bis.csv'
    
    complete_df = pd.read_csv(path_to_input_data)
    
    selected_df_bis = dataops.select_data_ndays_ago(data = complete_df, ndays = 3660, start = 367)
    loaded_data_bis = dataops.load(target_file = path_to_output_data_bis, data_to_load = selected_df_bis)
    
    selected_df = dataops.select_data_ndays_ago(data = complete_df, ndays = 3660, start = 1)
    loaded_data = dataops.load(target_file = path_to_output_data, data_to_load = selected_df)
    print('\n', selected_df.head(10))
    


def extract_eval_data():
    path_to_input_data = '/home/airflow/complete-processed-dataset/processed-weather-aus-up-to-date.csv'
    path_to_output_data = '/home/airflow/eval-data/eval-data.csv'
    
    complete_df = pd.read_csv(path_to_input_data)
    selected_df = dataops.select_data_ndays_ago(data = complete_df, ndays = 366, start = 1)
    
    loaded_data = dataops.load(target_file = path_to_output_data, data_to_load = selected_df)
    print('\n', selected_df.head(10))



def generate_eda_report_eval_data():
    path_to_input_data = '/home/airflow/eval-data/eval-data.csv'
    path_to_output_file = '/home/airflow/report-eda/eda-report-eval-data.html'
    
    title = "Analyse exploratoire des données météorologiques en Australie correspondant aux 366 derniers jours"
    data = pd.read_csv(path_to_input_data)
    dataops.generate_eda_report(data = data, title = title, output_file = path_to_output_file)



def generate_eda_report_train_data():
    path_to_input_data = '/home/airflow/train-data/train-data-bis.csv'
    path_to_output_file = '/home/airflow/report-eda/eda-report-train-data.html'
    
    title = "Analyse exploratoire des données météorologiques en Australie correspondant aux 3660 derniers jours avant les 366 jours de la date actuelle."
    data = pd.read_csv(path_to_input_data)
    dataops.generate_eda_report(data = data, title = title, output_file = path_to_output_file)



def train_logistic_regression_model(task_instance): 
    path_to_input_data = '/home/airflow/train-data/train-data.csv'
    path_to_score = '/home/airflow/score_lr.pkl'
    X, y = modelsops.read_and_prepare_data(input_path = path_to_input_data)
    
    estimator_lr = LogisticRegression(random_state=None, max_iter=200, class_weight="balanced", n_jobs=-1)
    score_lr = modelsops.compute_accuracy_score(estimator = estimator_lr, X = X, y = y)
    task_instance.xcom_push(key="xcom_score_lr",value=score_lr)
    print("the model score ", score_lr, ' is saved at ', path_to_score)
    pickle.dump(score_lr, open(path_to_score, 'wb'))
    
    
    
def train_extreme_gradient_boosting_model(task_instance):
    path_to_input_data = '/home/airflow/train-data/train-data.csv'
    path_to_score = '/home/airflow/score_xgb.pkl'
    X, y = modelsops.read_and_prepare_data(input_path = path_to_input_data)
    
    rate = y.value_counts()[0]/y.value_counts()[1]
    estimator_xgb = XGBClassifier(random_state=None, scale_pos_weight = rate, n_estimators=100, n_jobs=-1)
    score_xgb = modelsops.compute_accuracy_score(estimator = estimator_xgb, X = X, y = y)
    task_instance.xcom_push(key="xcom_score_xgb",value=score_xgb)
    print("the model score ", score_xgb, ' is saved at ', path_to_score)
    pickle.dump(score_xgb, open(path_to_score, 'wb'))
    


def select_best_model(task_instance):
    path_to_model_file = '/home/airflow/models/best-model-pipe.pkl'
    path_to_model_file_bis = '/home/airflow/models/best-model-pipe-bis.pkl'
    
    path_to_input_data = '/home/airflow/train-data/train-data.csv'
    path_to_input_data_bis = '/home/airflow/train-data/train-data-bis.csv'
    
    X, y = modelsops.read_and_prepare_data(input_path = path_to_input_data)
    X_bis, y_bis = modelsops.read_and_prepare_data(input_path = path_to_input_data_bis)
    
    #score_lr = task_instance.xcom_pull(key="xcom_score_lr",task_ids=['train_logistic_regression_model_task'])
    #score_xgb = task_instance.xcom_pull(key="xcom_score_xgb",task_ids=['train_extreme_gradient_boosting_model_task'])
    
    score_lr = pickle.load(open('/home/airflow/score_lr.pkl', 'rb'))
    score_xgb = pickle.load(open('/home/airflow/score_xgb.pkl', 'rb'))
    
    if  score_xgb < score_lr:
        estimator_lr = LogisticRegression(random_state=None, max_iter=200, class_weight="balanced", n_jobs=-1)
        modelsops.estimate_and_save_ml_model_pipeline(estimator = estimator_lr, X = X, y = y, output_path = path_to_model_file)
        modelsops.estimate_and_save_ml_model_pipeline(estimator = estimator_lr, X = X_bis, y = y_bis, output_path = path_to_model_file_bis)
    else:
        rate = y.value_counts()[0]/y.value_counts()[1]
        estimator_xgb = XGBClassifier(random_state=None, scale_pos_weight = rate, n_estimators=100, n_jobs=-1)
        modelsops.estimate_and_save_ml_model_pipeline(estimator = estimator_xgb, X = X, y = y, output_path = path_to_model_file)
        
        rate_bis = y_bis.value_counts()[0]/y_bis.value_counts()[1]
        estimator_xgb_bis = XGBClassifier(random_state=None, scale_pos_weight = rate_bis, n_estimators=100, n_jobs=-1)
        modelsops.estimate_and_save_ml_model_pipeline(estimator = estimator_xgb_bis, X = X_bis, y = y_bis, output_path = path_to_model_file_bis)



def generate_model_report_eval_data():
    path_to_output_file = '/home/airflow/model-evaluation/classification_report_eval.json'
    path_to_model_file = '/home/airflow/models/best-model-pipe-bis.pkl'
    path_to_input_data = '/home/airflow/eval-data/eval-data.csv'

    X_test, y_test = modelsops.read_and_prepare_data(input_path = path_to_input_data)
    pickled_best_model = modelsops.load_saved_estimated_ml_model_pipeline(input_path = path_to_model_file)
    predictions = pickled_best_model.predict(X_test)
    modelsops.compute_and_save_classification_report(y_true = y_test, y_pred = predictions, ouput_path = path_to_output_file)



def generate_model_report_train_data():
    path_to_output_file = '/home/airflow/model-evaluation/classification_report_train.json'
    path_to_output_file_bis = '/home/airflow/model-evaluation/classification_report_train_bis.json'
    path_to_model_file = '/home/airflow/models/best-model-pipe.pkl'
    path_to_model_file_bis = '/home/airflow/models/best-model-pipe-bis.pkl'
    path_to_input_data = '/home/airflow/train-data/train-data.csv'
    path_to_input_data_bis = '/home/airflow/train-data/train-data-bis.csv'

    X_test, y_test = modelsops.read_and_prepare_data(input_path = path_to_input_data)
    pickled_best_model = modelsops.load_saved_estimated_ml_model_pipeline(input_path = path_to_model_file)
    predictions = pickled_best_model.predict(X_test)
    modelsops.compute_and_save_classification_report(y_true = y_test, y_pred = predictions, ouput_path = path_to_output_file)
    
    X_test_bis, y_test_bis = modelsops.read_and_prepare_data(input_path = path_to_input_data_bis)
    pickled_best_model_bis = modelsops.load_saved_estimated_ml_model_pipeline(input_path = path_to_model_file_bis)
    predictions_bis = pickled_best_model.predict(X_test_bis)
    modelsops.compute_and_save_classification_report(y_true = y_test_bis, y_pred = predictions_bis, ouput_path = path_to_output_file_bis)
    



def decide_workflow():
    directory = '/home/airflow/complete-processed-dataset/processed-weather-aus-up-to-date.csv'
    if not os.path.exists(directory):
        return 'run_initialisation_workflow_task'
    else:
        return 'run_actualization_workflow_task'    



#---------------------------------------------------------------------------------------
# "0 */3 * * *"
#---------------------------------------------------------------------------------------



default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(0)
    }
    

with DAG(
    dag_id="FullMachineLearningOperationPipeline_dag", 
    default_args=default_args, 
    description='This is the dag which runs every three hours to update both weather data and model even from scratch.',
    tags=['mlops', 'datascientest'],
    schedule_interval=None,    
    catchup = False) as dag:
    
    
    start = BashOperator( 
        task_id="start",
        bash_command="echo This is the beginning of the mlops workflow."
        )
          
    
    download_current_month_data_task = BashOperator( 
        task_id="download_current_month_data_task",
        bash_command="scripts/download_current_month_data.sh"
        )
    
    
    download_ongoing_month_data_task = BashOperator( 
        task_id="download_ongoing_month_data_task",
        bash_command="scripts/download_current_month_data.sh"
        )
    
    
    download_previous_month_data_task = BashOperator( 
        task_id="download_previous_month_data_task",
        bash_command="scripts/download_past_first_month_data.sh"
        )
            

    transform_ongoing_and_previous_month_data_task = PythonOperator( 
        task_id="transform_ongoing_and_previous_month_data_task",
        python_callable=transform_ongoing_and_previous_month_data,
        provide_context=True
        )
    
    
    update_weather_database_task = PythonOperator( 
        task_id="update_weather_database_task",
        python_callable=update_weather_database,
        provide_context=True
        )
    
    
    download_past_historical_data_task = BashOperator( 
        task_id="download_past_historical_data_task",
        bash_command="scripts/download_past_historical_data.sh"
        )
        
         
    download_past_first_month_data_task = BashOperator( 
        task_id="download_past_first_month_data_task",
        bash_command="scripts/download_past_first_month_data.sh"
        )
        
    
    download_past_second_month_data_task = BashOperator( 
        task_id="download_past_second_month_data_task",
        bash_command="scripts/download_past_second_month_data.sh"
        )
    
    
    download_past_third_month_data_task = BashOperator( 
        task_id="download_past_third_month_data_task",
        bash_command="scripts/download_past_third_month_data.sh"
        )
        
        
    download_past_fourth_month_data_task = BashOperator( 
        task_id="download_past_fourth_month_data_task",
        bash_command="scripts/download_past_fourth_month_data.sh"
        )
    
    
    download_past_fifth_month_data_task = BashOperator( 
        task_id="download_past_fifth_month_data_task",
        bash_command="scripts/download_past_fifth_month_data.sh"
        )
    
    
    download_past_sixth_month_data_task = BashOperator( 
        task_id="download_past_sixth_month_data_task",
        bash_command="scripts/download_past_sixth_month_data.sh"
        )
    
    
    download_past_seventh_month_data_task = BashOperator( 
        task_id="download_past_seventh_month_data_task",
        bash_command="scripts/download_past_seventh_month_data.sh"
        )
        

    download_past_eighth_month_data_task = BashOperator( 
        task_id="download_past_eighth_month_data_task",
        bash_command="scripts/download_past_eighth_month_data.sh"
        )
        
 
    download_past_ninth_month_data_task = BashOperator( 
        task_id="download_past_ninth_month_data_task",
        bash_command="scripts/download_past_ninth_month_data.sh"
        )
        

    download_past_tenth_month_data_task = BashOperator( 
        task_id="download_past_tenth_month_data_task",
        bash_command="scripts/download_past_tenth_month_data.sh"
        )
        

    download_past_eleventh_month_data_task = BashOperator( 
        task_id="download_past_eleventh_month_data_task",
        bash_command="scripts/download_past_eleventh_month_data.sh"
        )
        

    download_past_twelfth_month_data_task = BashOperator( 
        task_id="download_past_twelfth_month_data_task",
        bash_command="scripts/download_past_twelfth_month_data.sh"
        )
        

    download_past_thirteenth_month_data_task = BashOperator( 
        task_id="download_past_thirteenth_month_data_task",
        bash_command="scripts/download_past_thirteenth_month_data.sh"
        )
    

    transform_historical_data_task = PythonOperator( 
        task_id="transform_historical_data_task",
        python_callable=transform_historical_data,
        provide_context=True
        )

    
    transform_last_fourteen_month_data_task = PythonOperator( 
        task_id="transform_last_fourteen_month_data_task",
        python_callable=transform_last_fourteen_month_data,
        provide_context=True
        )
    

    merge_historical_with_last_fourteen_month_data_task = PythonOperator( 
        task_id="merge_historical_with_last_fourteen_month_data_task",
        python_callable=merge_historical_with_last_fourteen_month_data,
        provide_context=True
        )
        

    extract_train_data_task = PythonOperator( 
        task_id="extract_train_data_task",
        trigger_rule = "one_success",
        python_callable=extract_train_data,
        provide_context=True
        )
    

    extract_eval_data_task = PythonOperator( 
        task_id="extract_eval_data_task",
        trigger_rule = "one_success",
        python_callable=extract_eval_data,
        provide_context=True
        )
    
    
    generate_eda_report_eval_data_task = PythonOperator( 
        task_id="generate_eda_report_eval_data_task",
        python_callable=generate_eda_report_eval_data,
        provide_context=True
        )
    

    generate_eda_report_train_data_task = PythonOperator( 
        task_id="generate_eda_report_train_data_task",
        python_callable=generate_eda_report_train_data,
        provide_context=True
        )
    

    train_logistic_regression_model_task = PythonOperator( 
        task_id="train_logistic_regression_model_task",
        python_callable=train_logistic_regression_model,
        provide_context=True
        )
        

    train_extreme_gradient_boosting_model_task = PythonOperator( 
        task_id="train_extreme_gradient_boosting_model_task",
        python_callable=train_extreme_gradient_boosting_model,
        provide_context=True
        )
        

    select_best_model_task = PythonOperator( 
        task_id="select_best_model_task",
        python_callable=select_best_model,
        provide_context=True
        )
        

    generate_model_report_eval_data_task = PythonOperator( 
        task_id="generate_model_report_eval_data_task",
        python_callable=generate_model_report_eval_data,
        provide_context=True
        )
        
        
    generate_model_report_train_data_task = PythonOperator( 
        task_id="generate_model_report_train_data_task",
        python_callable=generate_model_report_train_data,
        provide_context=True
        )    
    
        
        
    decide_workflow_task = BranchPythonOperator(
       task_id='decide_workflow_task',
       provide_context=True,
       python_callable=decide_workflow,
        ) 
        
           
    run_initialisation_workflow_task = BashOperator( 
            task_id="run_initialisation_workflow_task",
            bash_command="echo The initialization workflow is running."
        )



    run_actualization_workflow_task = BashOperator( 
                task_id="run_actualization_workflow_task",
                bash_command="echo The actualization workflow is running."
            )
        
        
    finish = BashOperator( 
        task_id="finish",
        trigger_rule = "all_success",
        bash_command="echo This is the end of the mlops workflow."
        )
    
    
    
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
    
    
    
start >> decide_workflow_task >> run_initialisation_workflow_task    

run_initialisation_workflow_task >> [
    download_current_month_data_task,
    download_past_first_month_data_task, 
    download_past_second_month_data_task,
    download_past_third_month_data_task,
    download_past_fourth_month_data_task,
    download_past_fifth_month_data_task,
    download_past_sixth_month_data_task,
    download_past_seventh_month_data_task,
    download_past_eighth_month_data_task,
    download_past_ninth_month_data_task,
    download_past_tenth_month_data_task,
    download_past_eleventh_month_data_task,
    download_past_twelfth_month_data_task,
    download_past_thirteenth_month_data_task
    ] 


[
    download_current_month_data_task,
    download_past_first_month_data_task, 
    download_past_second_month_data_task,
    download_past_third_month_data_task,
    download_past_fourth_month_data_task,
    download_past_fifth_month_data_task,
    download_past_sixth_month_data_task,
    download_past_seventh_month_data_task,
    download_past_eighth_month_data_task,
    download_past_ninth_month_data_task,
    download_past_tenth_month_data_task,
    download_past_eleventh_month_data_task,
    download_past_twelfth_month_data_task,
    download_past_thirteenth_month_data_task
    ] >> transform_last_fourteen_month_data_task


start >> decide_workflow_task >> run_initialisation_workflow_task

run_initialisation_workflow_task >> download_past_historical_data_task >> transform_historical_data_task

[transform_historical_data_task, transform_last_fourteen_month_data_task] >> merge_historical_with_last_fourteen_month_data_task

merge_historical_with_last_fourteen_month_data_task >> extract_train_data_task

merge_historical_with_last_fourteen_month_data_task >> extract_eval_data_task

extract_train_data_task >> generate_eda_report_train_data_task >> finish

extract_eval_data_task >> generate_eda_report_eval_data_task >> finish

extract_train_data_task >> [train_logistic_regression_model_task, train_extreme_gradient_boosting_model_task] >> select_best_model_task

[select_best_model_task, extract_eval_data_task] >> generate_model_report_eval_data_task >> finish

select_best_model_task >> generate_model_report_train_data_task >> finish




#---------------------------------------------------------------------------------------






start >> decide_workflow_task >> run_actualization_workflow_task

run_actualization_workflow_task >> [download_ongoing_month_data_task, download_previous_month_data_task] >> transform_ongoing_and_previous_month_data_task

transform_ongoing_and_previous_month_data_task >> update_weather_database_task >> [extract_eval_data_task, extract_train_data_task]

extract_train_data_task >> generate_eda_report_train_data_task >> finish

extract_eval_data_task >> generate_eda_report_eval_data_task >> finish

extract_train_data_task >> [train_logistic_regression_model_task, train_extreme_gradient_boosting_model_task] >> select_best_model_task

[select_best_model_task, extract_eval_data_task] >> generate_model_report_eval_data_task >> finish

select_best_model_task >> generate_model_report_train_data_task >> finish




#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

