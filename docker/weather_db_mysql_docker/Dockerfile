FROM mysql:latest

WORKDIR /home/data/

RUN echo [mysqld] >> /etc/mysql/conf.d/mysqld.cnf && \
    echo secure-file-priv="/home/data/" >> /etc/mysql/conf.d/mysqld.cnf && \
    echo local_infile=1 >> /etc/mysql/conf.d/mysqld.cnf

COPY ./processed-weather-aus-up-to-date.csv ./

COPY ./1.0-pdkengne-weather-db.sql /docker-entrypoint-initdb.d/

