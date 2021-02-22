"""This script converts data from Sidra PAM to a csv file that can be uploaded
to the table Prod_Municipal. This script works only if the files with data have
the same format. Therefore, when taking data from Sidra PAM ensure that all files
have the same year, crops and locations values."""

from pandas import read_csv
from pandas import DataFrame
from os import listdir
from os import remove
from os import path
import sidra_functions as sf

columnsIn = ["Município", "Ano", "Lavoura", "Variável", "Valor"]
columnsMustCSV = ["Cultura", "Ano", "Área Plantada",\
"Área Colhida", "Qtd.Produzida", "Valor Produção (Moeda em Real)",\
"Município"]

outCSV = DataFrame(columns = columnsMustCSV)

if path.exists('outFile.csv'):
	remove('outFile.csv')

for file in listdir():
	
	#check if file is csv
	if (file.split('.')[-1] == "csv"):
	
		tmp_csv = read_csv(file, names = columnsIn, skiprows = 2)

		if (read_csv(file, skiprows = 1).columns[0]=="Ano"):
			tmp_csv = tmp_csv.rename(\
			columns = {"Ano":"Município", "Município":"Ano"})
			
		#Drop rows where lavoura = Total
		tmp_csv=tmp_csv[tmp_csv["Lavoura"]!="Total"]
		tmp_csv.reset_index(inplace = True, drop = True)
		tmp_csv.sort_values(inplace = True, by = ["Ano","Município","Lavoura"])
		
		#get variable type if it's production, harvested area, ...
		variavel = tmp_csv["Variável"][0].lower()

		#mapping values on columns
		if(str(variavel).find("área colhida")!=-1):
			outCSV["Área Colhida"] = tmp_csv["Valor"]
				
		if(str(variavel).find("área plantada")!=-1):
			outCSV["Área Plantada"] = tmp_csv["Valor"]
				
		if(str(variavel).find("produzida")!=-1):
			outCSV["Qtd.Produzida"] = tmp_csv["Valor"]			

		if(str(variavel).find("valor da produção")!=-1):
			outCSV["Valor Produção (Moeda em Real)"] = tmp_csv["Valor"]

#Mapping city, year and crops	
outCSV["Município"] = tmp_csv["Município"]
outCSV["Ano"] = tmp_csv["Ano"]
outCSV["Cultura"] = tmp_csv["Lavoura"]

#clean data
outCSV = sf.clean_csv(outCSV)

outCSV.to_csv("outFile.csv", index = False)
