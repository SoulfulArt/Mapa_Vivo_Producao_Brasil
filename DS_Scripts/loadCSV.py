'''
This script load all csv files in the current path to the table Prod_Municipal.
The CSV files must be in the same folder where the script is being executed.
The CSV file must also has at least these columns "Nome Lavoura",
"Município", "Ano", "Área Colhida(em Milhares de Hectares)","Qtd.Produzida(em 
Mil Toneladas)", "Rendimento Médio", "Valor Produção (em Milhares de R$)" and 
"Município". This pattern of column names was choosen because the site where the
data will be taken from use these column names.
'''

from os import listdir
from os import remove
from os import path
from pandas import read_csv
from pandas import DataFrame
from getpass import getpass
from pymysql import connect

password = getpass("Type password:\n")
host = input("Type domain:\n")
userName = input("Type user:")

#Connecting to mysql server
myCon = connect(user = userName, port = 3306, password = password,\
host = host, database = "BRAZILDS", local_infile = True)

#sqlCMD will execute querries
sqlCMD = myCon.cursor()

#get the last Prod_ID
sqlCMD.execute("Select MAX(Prod_ID) FROM Prod_Municipal;")
last_ID = sqlCMD.fetchall()[0][0]
if last_ID == None: last_ID = 0

#Load CSV file into table Prod_Municipal
loadCSV = '''LOAD DATA LOCAL INFILE  'Prod_Municipal.csv' 
INTO TABLE Prod_Municipal FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\n';'''

#Columns in the table Prod_Municipal
columnsTbl = ["Prod_ID", "Cultura", "Ano", "Area", "Producao", "Rendimento",\
"Valor", "Municipio_ID"]

#Get Municipios ID

municipios = read_csv("MunMicroMeso.csv")

#it will be necessary when compare datasets to use lower cases
municipios["Municipio_Meso_Micro"] = municipios["Municipio_Meso_Micro"].apply(lambda k: k.lower())

#Municipios that doesn't exist in municipios
failMun = []

#Columns that csv file must contain

columnsMustCSV = ["Nome Lavoura", "Ano", "Área Colhida(em Milhares de Hectares)",\
"Qtd.Produzida(em Mil Toneladas)", "Rendimento Médio", "Valor Produção (em Milhares de R$)",\
"Município"]

#Bool to check if file has necessary columns
fileNotOk = False
filesNotOk = []
if path.exists("failFiles.txt"):
	remove("failFiles.txt") #remove failFiles if exists

if path.exists("loadedFiles.txt"):
	remove("loadedFiles.txt") #remove loadedFiles if exists

if path.exists("failedMun.txt"):
	remove("failedMun.txt") #remove failedMun if exists

if path.exists("Prod_Municipal.csv"):
	remove("Prod_Municipal.csv") #remove failedMun if exists

#Dataframe df_SQL will be used as input to mysql table Prod_Municipal
df_SQL = DataFrame(columns = columnsTbl)

#Get all csv files in the current path
for file in listdir():
	
	#check if file is csv
	if (file.split('.')[-1] == "csv" and\
	file.split('.')[0]!="MunMicroMeso" and\
	file.split('.')[0]!="Prod_Municipal"):
		
		tmp_csv = read_csv(file)
		tmp_csv = tmp_csv.dropna() #drop rows with null values
		tmp_csv = tmp_csv.reset_index(drop = True)
	
	#check if file countains necessary columns
		for k in columnsMustCSV:

			if k in tmp_csv.columns:
				fileNotOk = False

			else:
				fileNotOk = True
				filesNotOk.append(file)
				break

		if fileNotOk:
			print("File "+file.split('.')[0]+" doesn't have necessary columns")
			with open ('failFiles.txt', 'a') as writer:
				writer.write(file+"\n")

			continue

		#mapping columns from csv file to the df_SQL
		df_SQL["Cultura"] = tmp_csv["Nome Lavoura"]
		df_SQL["Ano"] = tmp_csv["Ano"]
		df_SQL["Area"] = tmp_csv["Área Colhida(em Milhares de Hectares)"]
		df_SQL["Producao"] = tmp_csv["Qtd.Produzida(em Mil Toneladas)"]
		df_SQL["Rendimento"] = tmp_csv["Rendimento Médio"]
		df_SQL["Valor"] = tmp_csv["Valor Produção (em Milhares de R$)"]
		df_SQL["Municipio_ID"] = tmp_csv["Município"].map(str.lower) + \
		tmp_csv["Microrregião"].map(str.lower)  + \
		tmp_csv["Mesorregião"].map(str.lower)
		df_SQL["Municipio_ID"] = df_SQL["Municipio_ID"].str.replace('/',' e ')	

		#mapping muncipios names to id
		df_SQL["Municipio_ID"] = df_SQL["Municipio_ID"].apply(lambda k:\
		municipios.Municipio_ID.loc[municipios.Municipio_Meso_Micro == k].values[0]\
		if len(municipios.Municipio_ID.loc[municipios.Municipio_Meso_Micro == k]) != 0\
		else failMun.append(k))

		#Print municipios that were not found
		if len (failMun) > 0:
			print(file+" some municipios not found check failedMun.txt")
			
			failMun = list(dict.fromkeys(failMun)) #remove duplicates
			with open('failedMun.txt', 'w') as writer:
				for i in failMun:				
					writer.write(file+":"+i+"\n")
	
		else:	
			#Insert Pib_ID starting from the last ID in the table Prod_Municipal
			df_SQL['Prod_ID'] = df_SQL.index + last_ID + 1
			last_ID = df_SQL.iloc[-1,0]
		
			df_SQL.to_csv('Prod_Municipal.csv', index = False,\
			header = False, mode = 'a')
			sqlCMD.execute(loadCSV)
			print(myCon.show_warnings())
			myCon.commit()

			#create new empty dataframe
			df_SQL = DataFrame(columns = columnsTbl)

			with open ('loadedFiles.txt', 'a') as writer:
				writer.write(file+"\n")

		failMun = []
		fileNotOk = False

#close mysql connection
myCon.close()
