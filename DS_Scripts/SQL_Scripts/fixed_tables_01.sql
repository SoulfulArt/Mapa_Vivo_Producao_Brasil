/*
This script load data for the tables of this project
To work properly csv files should be on the same directory where the script is 
being executed. These files shall be named Estados, Mesorregiao, Microrregiao,
Municipios and must be csv files.
*/

INSERT INTO Regiao VALUES 

	(1, 'Norte', 'N'),
	(2, 'Nordeste', 'NE'),
	(3, 'Centro-Oeste','CO'),
	(4, 'Sudeste', 'SE'),
	(5, 'Sul', 'S');
	
/*Load data from CSV files*/

LOAD DATA LOCAL INFILE  'Culturas.csv' INTO TABLE Culturas
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE  'Estados.csv' INTO TABLE Estados
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE  'Mesorregiao.csv' INTO TABLE Mesorregiao
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE  'Microrregiao.csv' INTO TABLE Microrregiao
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE  'Municipios.csv' INTO TABLE Municipios
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE  'Pib_Municipal.csv' INTO TABLE Pib_Municipal
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
