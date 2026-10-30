CREATE DATABASE IF NOT EXISTS weather;

use weather;

CREATE TABLE IF NOT EXISTS weathers(
    location enum ('Albury', 'BadgerysCreek', 'Cobar', 'CoffsHarbour', 'Moree',
        'Newcastle', 'NorahHead', 'NorfolkIsland', 'Penrith', 'Richmond',
        'Sydney', 'SydneyAirport', 'WaggaWagga', 'Williamtown',
        'Wollongong', 'Canberra', 'Tuggeranong', 'MountGinini', 'Ballarat',
        'Bendigo', 'Sale', 'MelbourneAirport', 'Melbourne', 'Mildura',
        'Nhil', 'Portland', 'Watsonia', 'Dartmoor', 'Brisbane', 'Cairns',
        'GoldCoast', 'Townsville', 'Adelaide', 'MountGambier', 'Nuriootpa',
        'Woomera', 'Albany', 'Witchcliffe', 'PearceRAAF', 'PerthAirport',
        'Perth', 'SalmonGums', 'Walpole', 'Hobart', 'Launceston',
        'AliceSprings', 'Darwin', 'Katherine', 'Uluru') NOT NULL,
    mintemp REAL,
    maxtemp REAL,
    rainfall REAL,
    evaporation REAL,
    sunshine REAL,
    windgustdir enum ('W', 'WNW', 'WSW', 'NE', 'NNW', 'N', 'NNE', 'SW', 'nan', 'ENE','SSE', 'S', 'NW', 'SE', 'ESE', 'E', 'SSW', ''),
    windgustspeed REAL,
    winddir9am enum ('W', 'NNW', 'SE', 'ENE', 'SW', 'SSE', 'S', 'NE', 'nan', 'SSW', 'N', 'WSW', 'ESE', 'E', 'NW', 'WNW', 'NNE', ''),
    winddir3pm enum ('WNW', 'WSW', 'E', 'NW', 'W', 'SSE', 'ESE', 'ENE', 'NNW', 'SSW', 'SW', 'SE', 'N', 'S', 'NNE', 'nan', 'NE', ''),
    windspeed9am REAL,
    windspeed3pm REAL,
    humidity9am REAL,
    humidity3pm REAL,
    pressure9am REAL,
    pressure3pm REAL,
    cloud9am REAL,
    cloud3pm REAL,
    temp9am REAL,
    temp3pm REAL,
    raintoday enum ('No', 'Yes'),
    raintomorrow enum ('No', 'Yes'),
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    PRIMARY KEY (location, year, month, day)
    );

SET PERSIST local_infile = 1;

LOAD DATA INFILE '/home/data/processed-weather-aus-up-to-date.csv' INTO TABLE weathers
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES
    (@vlocation, @vmintemp, @vmaxtemp, @vrainfall, @vevaporation, @vsunshine, @vwindgustdir, @vwindgustspeed, @vwinddir9am, @vwinddir3pm, @vwindspeed9am, @vwindspeed3pm, @vhumidity9am, @vhumidity3pm,@vpressure9am, @vpressure3pm, @vcloud9am, @vcloud3pm, @vtemp9am, @vtemp3pm, @vraintoday, @vraintomorrow, @vyear, @vmonth, @vday
    )
    SET
    location = NULLIF(@vlocation,''), mintemp = NULLIF(@vmintemp,''), maxtemp = NULLIF(@vmaxtemp,''), rainfall = NULLIF(@vrainfall,''), 
    evaporation = NULLIF(@vevaporation,''), sunshine = NULLIF(@vsunshine,''), windgustdir = NULLIF(@vwindgustdir,''), windgustspeed = NULLIF(@vwindgustspeed,''), 
    winddir9am = NULLIF(@vwinddir9am,''), winddir3pm = NULLIF(@vwinddir3pm,''), windspeed9am = NULLIF(@vwindspeed9am,''), windspeed3pm = NULLIF(@vwindspeed3pm,''), 
    humidity9am = NULLIF(@vhumidity9am,''), humidity3pm = NULLIF(@vhumidity3pm,''), pressure9am = NULLIF(@vpressure9am,''), pressure3pm = NULLIF(@vpressure3pm,''), 
    cloud9am = NULLIF(@vcloud9am,''), cloud3pm = NULLIF(@vcloud3pm,''), temp9am = NULLIF(@vtemp9am,''), temp3pm = NULLIF(@vtemp3pm,''), 
    raintoday = NULLIF(@vraintoday,''), raintomorrow = NULLIF(@vraintomorrow,'') , year = NULLIF(@vyear,''), month = NULLIF(@vmonth,''), day = NULLIF(@vday,'');



