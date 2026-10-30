FROM apache/airflow:2.6.3-python3.10

COPY ./requirements.txt ./

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" scikit-learn==1.2.2 xgboost pandas ydata-profiling requests httpie matplotlib seaborn mlxtend SQLAlchemy PyMySQL pytest opendatasets

#RUN pip3 install --no-cache-dir -r requirements.txt
