CREATE DATABASE IF NOT EXISTS user;

use user;

CREATE TABLE IF NOT EXISTS users(
    userid int not null AUTO_INCREMENT,
    first_name varchar(100),
    last_name  varchar(100),
    email  varchar(50),
    username  varchar(50),
    password varchar(50),
    role  varchar(50),
    PRIMARY KEY (userid)   
    );
    
 INSERT INTO users(first_name, last_name, email, username, password, role)
 VALUES
     ('gregory', 'herre', 'gregory.herre@gmail.com', 'hgregory', 'hgregory', 'admin'),
     ('matthieu', 'cazier', 'matthieucazier@hotmail.com', 'cmatthieu', 'cmatthieu', 'admin'),
     ('alain', 'sielenou', 'sielenou_alain@yahoo.fr', 'salain', 'salain', 'admin'),
     ('daniel', 'support', 'support@datascientest.com', 'sdaniel', 'sdaniel', 'standard'),
     ('sebastien', 'sime', 'sebastien.s@datascientest.com', 'ssebastien', 'ssebastien', 'standard'),
     ('admin', 'master', 'admin-master@domain.com', 'admin', 'master', 'admin');
