#This is a mysql script that creates the database and tables necessary to the
#project Mapa_Vivo_Produção_Agrícola_Brasil

CREATE DATABASE BRAZILDS;

USE BRAZILDS;

#Support tables
CREATE TABLE Culturas (

	Cultura_ID INT Primary Key NOT NULL,
	Cultura_Nome VARCHAR (32)

);


#Cidades e Regiões tables
CREATE TABLE Regiao (

	Regiao_ID INT Primary Key NOT NULL,
	Regiao_Nome VARCHAR (12),
	Regiao_Sigla VARCHAR (2)

);

CREATE TABLE Estados (

	Estado_ID INT Primary Key NOT NULL,
	Estado_Nome VARCHAR (22),
	Estado_Sigla VARCHAR (2),
	Regiao_ID INT,
	FOREIGN KEY (Regiao_ID) REFERENCES Regiao (Regiao_ID)

);

CREATE TABLE Mesorregiao (

	Mesorregiao_ID INT Primary Key NOT NULL,
	Mesorregiao_Nome VARCHAR (40),
	Estado_ID INT,
	FOREIGN KEY (Estado_ID) REFERENCES Estados (Estado_ID)

);

CREATE TABLE Microrregiao (

	Microrregiao_ID INT Primary Key NOT NULL,
	Microrregiao_Nome VARCHAR (40),
	Mesorregiao_ID INT,
	FOREIGN KEY (Mesorregiao_ID) REFERENCES Mesorregiao (Mesorregiao_ID)

);

CREATE TABLE Municipios (

	Municipio_ID INT Primary Key NOT NULL,
	Municipios_Nome VARCHAR (40),
	Microrregiao_ID INT,
	FOREIGN KEY (Microrregiao_ID) REFERENCES Microrregiao (Microrregiao_ID)

);


#Geografia Econômica tables
CREATE TABLE Pib_Municipal (

	PIB_ID INT PRIMARY KEY NOT NULL,
	ANO INT,
	PIB FLOAT,
	Populacao FLOAT,
	Per_Capita FLOAT,
	Municipio_ID INT,
	FOREIGN KEY (Municipio_ID) REFERENCES Municipios (Municipio_ID)

);

CREATE TABLE Prod_Municipal (

	Prod_ID INT PRIMARY KEY NOT NULL,
	Cultura_ID INT,
	ANO INT,
	AreaPlant FLOAT,
	AreaHarv FLOAT,
	Producao FLOAT,
	Rendimento FLOAT,
	Valor FLOAT,
	Municipio_ID INT,
	FOREIGN KEY (Cultura_ID) REFERENCES Culturas (Cultura_ID),
	FOREIGN KEY (Municipio_ID) REFERENCES Municipios (Municipio_ID)

);
