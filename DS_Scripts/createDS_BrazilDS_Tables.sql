#This is a mysql script that creates the database and tables necessary to the
#project Mapa_Vivo_Produção_Agrícola_Brasil

CREATE DATABASE BRAZILDS;

CREATE TABLE Regiao (

	Regiao_ID INT Primary Key NOT NULL,
	Regiao_Nome varchar (12),
	Regiao_Sigla varchar (2)

);

CREATE TABLE Estados (

	Estado_ID INT Primary Key NOT NULL,
	Estado_Nome varchar (22),
	Regiao_ID INT,
	FOREIGN KEY (Regiao_ID) REFERENCES Regiao (Regiao_ID)

);

CREATE TABLE Mesorregiao (

	Mesorregiao_ID INT Primary Key NOT NULL,
	Mesorregiao_Nome varchar (40),
	Estado_ID INT,
	FOREIGN KEY (Estado_ID) REFERENCES Estados (Estado_ID)

);

CREATE TABLE Microrregiao (

	Microrregiao_ID INT Primary Key NOT NULL,
	Microrregiao_Nome varchar (40),
	Mesorregiao_ID INT,
	FOREIGN KEY (Mesorregiao_ID) REFERENCES Mesorregiao (Mesorregiao_ID)

);

CREATE TABLE Municipios (

	Municipios_ID INT Primary Key NOT NULL,
	Municipios_Nome varchar (40),
	Microrregiao_ID INT,
	FOREIGN KEY (Microrregiao_ID) REFERENCES Microrregiao (Microrregiao_ID)

);
