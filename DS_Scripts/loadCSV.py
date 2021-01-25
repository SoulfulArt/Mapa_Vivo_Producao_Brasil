'''
This script load all csv files in the folder Dados to the table Prod_Municipal.
The CSV file must also has at least these columns "Nome Lavoura",
"Município", "Ano", "Área Colhida(em Milhares de Hectares)","Qtd.Produzida(em 
Mil Toneladas)", "Rendimento Médio", "Valor Produção (em Milhares de R$)" and 
"Município". This pattern of column names was choosen because the site where the
data will be taken from use these column names.
'''

from os import listdir
from os import environ
from os import removedirs
from pandas import read_csv
from pandas import DataFrame
from getpass import getpass
from pymysql import connect
import functionsLoadCSV as fl
from datetime import datetime
from shutil import rmtree

#get mysql parameters
password = getpass("Type password:\n")
host = input("Type domain:\n")
userName = input("Type user:\n")	

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
ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;'''

#Columns in the table Prod_Municipal
columnsTbl = ["Prod_ID", "Cultura", "Ano", "AreaP","AreaH", "Producao",\
"Rendimento", "Valor", "Municipio_ID"]

#Get current date
dateNow = str(datetime.now())

#Columns that csv file must contain

columnsMustCSV = ["Nome Lavoura", "Ano", "Área Colhida",\
"Qtd.Produzida", "Valor Produção (Moeda em Real)",\
"Nome Município IBGE"]

#Municipios that doesn't exist in municipios
failMun = []

#Culturas that doesn't exist on our database
failCult = []

#Bool to check if file has necessary columns
fileNotOk = False
filesNotOk = []

#Dataframe df_SQL will be used as input to mysql table Prod_Municipal
df_SQL = DataFrame(columns = columnsTbl)

dadosDir = environ["PWD"].replace("DS_Scripts","Data")

#Get Municipios ID
municipios = read_csv(dadosDir+"/MunMicroMeso.csv")

#Simplify text for better mapping
municipios["Municipio_Meso_Micro"] = fl.simplifyText(municipios["Municipio_Meso_Micro"])

#Get Culturas_ID
culturas = read_csv(dadosDir+"/Culturas.csv")

#Simplify text for better mapping
culturas["Nome"] = fl.simplifyText(culturas["Nome"])

#Get all csv files in the current path
for file in listdir('Dados/'):
	
	#check if file is csv
	if (file.split('.')[-1] == "csv"):
	
		#reset variables and dfs
		failMun = []
		failCult = []
		fileNotOk = False
		df_SQL = DataFrame(columns = columnsTbl)
		
		tmp_csv = fl.cleanDataCSV(read_csv('Dados/'+file))
		
		print("Loading file: "+file+" ...")
				
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
			with open ('Log_Files/failFiles'+dateNow+'.txt', 'a') as writer:
				writer.write(file+": no columns\n")
			continue
		
		if tmp_csv.empty:
			print("File "+file.split('.')[0]+" has no valuable data")	
			with open ('Log_Files/failFiles'+dateNow+'.txt', 'a') as writer:
				writer.write(file+":no valuable data\n")
			continue

		#mapping columns from csv file to the df_SQL
		df_SQL["Cultura"] = fl.simplifyText(tmp_csv["Nome Lavoura"])
		df_SQL["Ano"] = tmp_csv["Ano"]
		df_SQL["AreaP"] = 0
		df_SQL["AreaH"] = tmp_csv["Área Colhida"]
		df_SQL["Producao"] = tmp_csv["Qtd.Produzida"]
		df_SQL["Valor"] = tmp_csv["Valor Produção (Moeda em Real)"]
		df_SQL["Municipio_ID"] = tmp_csv["Nome Município IBGE"].astype(str) +\
		tmp_csv["Nome Microrregião"].astype(str)\
		+ tmp_csv["Nome Mesorregião"].astype(str)
		df_SQL["Municipio_ID"] = fl.simplifyText(df_SQL["Municipio_ID"])	
		df_SQL = fl.simplifyNumber(df_SQL)
		
		#mapping culturas to culturas_id
		df_SQL["Cultura"] = df_SQL["Cultura"].apply(lambda k:\
		culturas.ID.loc[culturas.Nome == k].values[0]\
		if len(culturas.ID.loc[culturas.Nome == k]) != 0\
		else failCult.append(k))

		#mapping muncipios names to id
		df_SQL["Municipio_ID"] = df_SQL["Municipio_ID"].astype(str)
		df_SQL["Municipio_ID"] = df_SQL["Municipio_ID"].apply(lambda k:\
		municipios.Municipio_ID.loc[municipios.Municipio_Meso_Micro == k].values[0]\
		if len(municipios.Municipio_ID.loc[municipios.Municipio_Meso_Micro == k]) != 0\
		else failMun.append(k))					

		#Print culturas that were not found
		failCult = list(dict.fromkeys(failCult)) #remove duplicates
		with open('Log_Files/failedCult'+dateNow+'.txt', 'a') as writer:
			for i in failCult:				
				writer.write(file+":"+str(i)+"\n")

		#Print municipios that were not found	
		failMun = list(dict.fromkeys(failMun)) #remove duplicates
		with open('Log_Files/failedMun'+dateNow+'.txt', 'a') as writer:
			for i in failMun:				
				writer.write(file+":"+i+"\n")
				
		if (len (failCult) > 0 and len (failMun) == 0):
			print(file+" some culturas not found check failedCult.txt")
			continue

		elif (len (failCult) == 0 and len (failMun) > 0):
			print(file+" some municipios not found check failedMun.txt")
			continue
			
		elif (len (failCult) > 0 and len (failMun) > 0):
			print(file+" some municipios not found check failedMun.txt")
			print(file+" some culturas not found check failedCult.txt")
			continue
			
		else:	
			#Insert Pib_ID starting from the last ID in the table Prod_Municipal
			df_SQL['Prod_ID'] = df_SQL.index + last_ID + 1
			last_ID = df_SQL.iloc[-1,0]

			#Culture_ID converted do int			
			df_SQL["Cultura"] = df_SQL["Cultura"].astype(int)
		
			df_SQL.to_csv('Prod_Municipal.csv', index = False)
			sqlCMD.execute(loadCSV)

			myCon.commit()

			if len(myCon.show_warnings()) == 0:
				print(file+" succesfully loaded with no warnings!")

			else: print(myCon.show_warnings())

			#create new empty dataframe
			df_SQL = DataFrame(columns = columnsTbl)

			with open ('Log_Files/loadedFiles'+dateNow+'.txt', 'a') as writer:
				writer.write(file+"\n")

rmtree("__pycache__")

#close mysql connection
myCon.close()
