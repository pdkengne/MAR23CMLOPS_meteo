# Prédiction de la météo avec l'API FastAPI

<img src="reports/images/image-1.png" alt="Alt text" title="Optional title">


Une API FastAPI a été mise en place pour permettre aux utilisateurs de prédire la météo en fonction de la ville et de la date spécifiées. L'API vérifie également l'identité de l'utilisateur avant de fournir les prédictions.



## Structure de l'environnement de développement



- **README.md:**   Ce fichier contient des informations générales concernant ce projet ainsi que son exploitation pratique par des développeurs ou tout public intéressé.

- **requirements.txt:**   Ce fichier contient les modules nécessaires à la  reproduction de l'environnement de travail. Il est généré à l'aide de la commande suivante: **`pip freeze > requirements.txt`**

- **datasets:** Ce dossier contient les données brutes issues de diverses sources externes ansi que les données nettoyées et transformées issues des analyses exploratoires.

- **models:** Ce dossier contient les artefacts associés aux modèles développés.

- **notebooks:** Ce dossier rassemble des notebooks au format jupyter qui contiennent des codes écrits en **Python**  permettant l'ingestion et l'analyse des données ansi que la construction des pipelines d'entrainement des algorithmes d'apprentissage automatique.

- **reports:**   Ce  dossier contient divers rapports d'analyse ainsi que des références aux formats HTML, PDF, etc.

- **docker:**   Ce dossier contient des codes pour la création des images permettant de générer des conteneurs docker afin d'isoler les services fournis par les technologies suivantes.
   - Les bases de données **MySQL** associées aux utilisateurs et aux données météorologiques. 
   - L'orchestrateur **Apache Airflow** de toutes les tâches associées au flux des traitements.
   - L'API développé à l'aide du module **FastAPI** qui offre aux utilisateurs la possibilité d'exploiter les services délivrés par le projet. 

- **fastapi:**  Ce dossier représente l'environnement de développement de notre API basé sur le module **FastAPI** de **Python.** A ce titre, il contient tous les fichiers de codes et des données necessaires pour son bon fonctionnement.

- **data-ingestion-pipeline:**  Ce dossier contient des codes d'extraction et de transformation des données brutes.

- **machine-learning-pipeline:**   Ce dossier contient des codes de construction des modèles prédictifs basés sur les algorithmes d'apprentissage automatique.

- **airflow:**  Ce dossier représente l'environnement d'orchestration de toutes les tâches associées au projet par la technologie **Airflow.** A ce titre, son sous dossier nommé **dags** contient deux modules nommés **`dataops.py`** et **`modelops.py`** qui rassemble les codes développés necessaires au bon fonctionnement des tâches.  Il contient également les codes relatifs à la définition du flux global des traitements que nous avons regroupés dans le fichier **`full_mlops_dag.py`.**
  
  
  
## Installation locale de l'environnement de travail


Pour avoir une copie opérationnelle du dépôt GitHub de ce projet sur votre ordinateur local, on peut suivre les instructions suivantes dans un terminal.

1. Effectuer le clonage du dépôt (si on a les droits) avec la commande suivante:

**`git clone https://github.com/DataScientest-Studio/MAR23CMLOPS_meteo.git`** 

2. Installer un module de virtualisation, par exemple `virtualenv` avec la commande suivante:

**`pip install virtualenv`**

3. Se déplacer dans le repertoire local du projet nommé `MAR23CMLOPS_meteo` avec la commande

**`cd MAR23CMLOPS_meteo`**

4. Créer un environnement virtuel nommé par exemple `projet_meteo_env` avec la commande suivante

**`virtualenv projet_meteo_env`**

5. Activer cet environnement à chaque fois qu'on souhaite y travailler avec la commande suivante

**`source projet_meteo_env/bin/activate`**

Précisions au passage qu'on peut se déconnecter de cet environnement en y exécutant la simple commande

**`deactivate`**

6. Installer tous les modules nécessaires à l'aide de la commande suivante

**`pip install -r requirements.txt`**

Précisons pour terminer que pour toutes activités ultérieures dans ce projet, seules les étapes 3. et 5. ci-dessus sont requises.




## Lancement de la plateforme Apache Airflow et de l'API


Nous avons personnalisé le fichier **`docker-compose.yaml`** de **`Airflow`** disponible en téléchargement avec la commande suivante

**`curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml'`**

Plus précisément, nous avons intégré dans ce fichier deux images docker préalablement construites.

- La première image nommée **`march2023mlops/airflow_docker:latest`** permet de générer un conteneur  docker d'Airflow qui inclut toutes les modules nécessaires pour faire fonctionner nos codes en **`Python`** et **`Bash`.** 

- La deuxième image nommée **`march2023mlops/api_raintomorrow:latest`** permet de générer un conteneur docker dans lequel l'API que nous avons développé fonctionne. 

Bien évidemment, nous avons définis dans le fichier **`docker-compose.yaml`** les volumes nécessaires qui permettent de synchroniser les échanges de données entre la machine hôte et les deux conteneurs mentionnés ci-dessus. 


Pour faire fonctionner correctement cette plateforme, on peut suivre les étapes ci-dessous.

1. Ouvrir un terminal, se rendre dans le dossier du projet **`MAR23CMLOPS_meteo,`** activer (si déactivé) l'environnement de travail associé au projet (**`virtualenv projet_meteo_env`**) et se déplacer dans le sous dossier **`airflow`** via la commande **`cd airflow`.**

2. Lors du tout premier lancement de la plateforme, il peut être nécessaire d'exécuter la suite des commandes suivantes.

**`echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`**

**`chmod -R 777 dags/`**

**`chmod -R 777 logs/`**

**`chmod -R 777 plugins/`**

**`chmod -R 777 config/`**

**`docker-compose up airflow-init`**

3. Une fois l'étape d'initialisation terminée, la plateforme se lance normalement avec la commande suivante

**`docker-compose up -d`**  

Précisons qu'on arrête le fonctionnement de la plateforme avec la commande suivante

**`docker-compose down`**

Nous terminons cette section en soulignant que pour tout lancement ultérieur de la plateforme, seules les étapes 1. et 3. ci-dessus sont requises. 



##  Utilisation de la plateforme Apache Airflow

Apache Airflow est une plate-forme open-source pour la programmation, la planification et la surveillance des workflows. Dans ce projet, nous utilisons Apache Airflow pour gérer le pipeline **`MLOps.`** 

Le pipeline **`MLOps`** est défini sous forme de tâches et de dépendances entre ces tâches. Chaque tâche représente une étape du flux de travail, comme la récupération des données météo, le prétraitement des données, l'entraînement du modèle, la réalisation des tests unitaires, l'évaluation des performances du modèle etc. La définition des dépendances entre les tâches permet de garantir leur exécution dans le bon ordre. Apache Airflow s'occupe de l'exécution automatique des tâches selon la planification ou les déclencheurs définis.


Dès lors que nous avons suivi avec succès les instructions de la section précédente relatives au lancement simultané de la plateforme Apache Airflow et de l'API, on peut se rendre (**quelques instants plus tard**) à la page suivante **[http://localhost:8080/](http://localhost:8080/)** dans un navigateur web de notre ordinateur pour obtenir la page présentée dans la figure ci-dessous. 

<img src="reports/images/Screenshot from 2023-07-24 06-32-56.png" alt="Alt text" title="Optional title">

Par défaut, Airflow nous permet de se connecter avec un compte dont le **`username`** est **`airflow`** et le **`password`** est **`airflow.`** Il suffit tout simplement de cliquer sur le bouton **`Sign In`** puisque ces informations sont pré-remplies.

On obtient la page ci-dessous sur laquelle on peut entrer comme filtre le tag **`datascientest`** ou **`mlops`** pour retrouver facilement notre DAG (directed acyclic graph) nommé **`FullMachineLearningOperationPipeline_dag`** qui contient le pipeline MLOps que nous avons mis en place.

<img src="reports/images/Screenshot from 2023-07-24 07-23-53.png" alt="Alt text" title="Optional title">

Pour lancer manuellement ce DAG, il faut cliquer sur son nom. Puis, dans la page ci-dessous qui va s'afficher, il faut l'activer en cliquant dans la case en haut et à gauche du nom du DAG. Enfin, il faut cliquer sur **`Trigger DAG`** en haut à droite après avoir cliquer sur l'icône du bouton `play.`

<img src="reports/images/Screenshot from 2023-07-24 07-43-14.png" alt="Alt text" title="Optional title">

Une fois lancer, on peut cliquer sur l'onglet nommé **`Graph`** pour visualiser le graphe associé au workflow. 
Le flux de travail que nous avons mis en place comprend deux flux de taĉhes dont un est le flux d'initialisation qui se ne s'exécute que si la base de données météorologiques est vide afin de l'alimenter automatiquement en données anciennes et récentes et d'estimer le modèle de prédiction à exploiter par l'API. Les tâches de couleur verte sur le diagramme ci-dessous représentent ce workflow. Les tâches de couleur rose sur ce même diagramme représentent quant à elles celles qui ne sont pas exécutées dans ce worflow.

<img src="reports/images/Screenshot from 2023-07-23 02-44-44.png" alt="Alt text" title="Optional title">


Dans le cas contraire, c'est l'autre flux de tâches qui va s'exécuter régulièrement selon le planning spécifié (par exemple, toutes les 3 heures) afin de mettre à jour la base de données et le modèle de prédiction en cours d'exploitation par l'API. Les tâches de couleur verte sur le diagramme ci-dessous représentent ce workflow. De même, les tâches de couleur rose sur ce même diagramme représentent quant à elles celles qui ne sont pas exécutées dans ce worflow.

<img src="reports/images/Screenshot from 2023-07-23 02-27-44.png" alt="Alt text" title="Optional title">


Notons que dans la phase d'ingestion, les données météorologiques  anciennes ou historiques sont automatiquement téléchargées depuis la page suivante [https://rdrr.io/cran/rattle.data/man/weatherAUS.html](https://rdrr.io/cran/rattle.data/man/weatherAUS.html). Par contre, les données récentes des `14` derniers mois (incluant le mois en cours) sont extraites par **web scraping** des différentes pages incluses dans site web suivant [http://www.bom.gov.au/climate/dwo/](http://www.bom.gov.au/climate/dwo/).
Tous les fichiers de codes `bash` d'ingestion de ces données se trouvent à l'emplacement **`./airflow/dags/scripts/`** à partir du repertoire **`MAR23CMLOPS_meteo`** associé au projet.



  
## Utilisation de l'API


Après l'exécution complète de notre workflow MLOps par Airflow, on peut se rendre à la page suivante **[http://localhost:8000/docs](http://localhost:8000/docs)** dans un navigateur web de notre ordinateur pour accéder à la documentation de l'API.  La figure ci-dessous montre les différentes routes ou points d'accès aux services proposés par cet API.  

<img src="reports/images/Screenshot from 2023-07-23 09-12-09.png" alt="Alt text" title="Optional title">

Cet API requiert de s'authentifier pour l'exploiter. Tout nouvel utilisateur peut se rendre sur la route **`sign-up`** pour créer un compte en remplissant au moins les deux champs obligatoires associés au **`username`** et au **`password`** comme indiqués sur la figure ci-dessous.

<img src="reports/images/Screenshot from 2023-07-23 21-16-44.png" alt="Alt text" title="Optional title">


Pour mieux comprendre les différents services proposés par notre API, il est indispensable de décrire les tâches qui sont réalisées dans le workflow MLOps sur **`Apache Airflow`** durant la phase d'entrainement des modèles de prédiction. 


Avant la phase d'entrainement des modèles de prédiction, `3` datasets sont extraites de la base de données.  Un de ces datasets sert  d'ensemble d'evaluation tandis que le deux autres  datasets servent à entrainer deux modèles différents. 

- Le dataset d'évaluation est constitué des données des `366` derniers jours avant le jour en cours. Un rapport d'analyse exploratoire sur ce dataset est généré dans le fichier **`eda-report-eval-data.html`** afin de surveiller l'évolution des distributions des données récentes et de les comparer à celles de données anciennes. Ce rapport est situé à l'emplacement **`./airflow/report-eda/.`**

- Le premier dataset d'entrainement est constitué des données des `3660` derniers jours avant le jour en cours. Le modèle entrainé sur ce dataset servira à réaliser la prévision météo sur la précipitation de pluie de la journée après une date complète donnée. La route **`/next-day-rain/forecast/ordinary`** de notre API expose ce service aux utilisateurs en leur demandant de spécifier uniquement la date et la ville concernées par cette prédiction (voir la figure ci-dessous). La route **`/next-day-rain/forecast/custom`** expose quant à elle le modèle aux utilisateurs experts et exploite plutôt les paramètres météorologiques renseignés par ces derniers en plus de la date et la ville concernée pour effectuer les prévisions. Les métriques quantifiant les performances de ce modèle sur les données d'entrainement sont accessibles sur la route **`/model/estimation-2`** de l'API.

<img src="reports/images/Screenshot from 2023-07-23 09-13-46.png" alt="Alt text" title="Optional title">


- Le deuxième dataset d'entrainement est constitué des données des `3660` derniers jours avant de la date associée à la `366`-ième journée du jour en cours. Un rapport d'analyse exploratoire sur ce dataset est généré dans le fichier **`eda-report-train-data.html`** pour permettre de comparer les distributions des données passées avec celles des données récentes. Ce rapport est également situé à l'emplacement **`./airflow/report-eda/.`** Le modèle entrainé sur ce dataset est testé sur l'ensemble d'évaluation. Une telle démarche sert à surveiller les métriques de performance des modèles entrainés sur `10` annnées de données à prédire correctement **(sans être mis à jours)** toutes les journées pluvieuses ou non durant la `11-`ième année. Les métriques quantifiant les performances de ce modèle sur les données d'entrainement sont accessibles sur la route **`/model/estimation-1`** de l'API tandis que les métriques quantifiant les performances de ce modèle sur les données d'évaluation sont accessibles sur la route **`/model/evaluation`** de l'API.



## Schéma de l'architecture globale 


<img src="reports/images/Screenshot from 2023-07-26 15-44-57.png" alt="Alt text" title="Optional title">



<!---
<img width="537" alt="image" src="https://github.com/DataScientest-Studio/MAR23CMLOPS_meteo/assets/61281716/c5d574ff-0d58-44fa-aa04-d76ae2351c9f">
-->


## Auteurs

- Auteur 1 (Pascal)
- Auteur 2 (Grégory)
- Auteur 3 (Matthieu)

## Mentor

- Sébastien

  






