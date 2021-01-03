#These are functions and variables that support script loadCSV.py

from os import remove
from os import path

#function that organize numerical data because some files use , as thousand
#separator or , as decimal separator

def simplifyNumber (df):
	
	df["Producao"] = df["Producao"].astype(str).str.replace(',','')
	df["Area"] = df["Area"].astype(str).str.replace(',','')
	df["Valor"] = df["Valor"].astype(str).str.replace(',','')

	df["Producao"] = df["Producao"].astype(float)
	df["Area"] = df["Area"].astype(float)
	df["Valor"] = df["Valor"].astype(float)

	return df

'''Function that replace letter with accent for letter without accent it can generate
problems in finding cities that are the same but has different accents from the
datasets. Other transformations that are specific of the data that is used in this
project such as '/' for ' e ' were identified as an important substituion to help
data manipulation through the project.'''

def simplifyText (pdSeries):
	
	#it's better to work with homgenous casing
	pdSeries = pdSeries.str.lower()

	#problems with accent in Portuguese
	pdSeries = pdSeries.str.replace('á','a')
	pdSeries = pdSeries.str.replace('ã','a')
	pdSeries = pdSeries.str.replace('â','a')
	pdSeries = pdSeries.str.replace('é','e')
	pdSeries = pdSeries.str.replace('ê','e')
	pdSeries = pdSeries.str.replace('í','i')
	pdSeries = pdSeries.str.replace('ó','o')
	pdSeries = pdSeries.str.replace('ô','o')
	pdSeries = pdSeries.str.replace('õ','o')
	pdSeries = pdSeries.str.replace('ú','u')
	pdSeries = pdSeries.str.replace('û','u')
	pdSeries = pdSeries.str.replace('ü','u')
	pdSeries = pdSeries.str.replace('j','g')
	pdSeries = pdSeries.str.replace('-','')
	pdSeries = pdSeries.str.replace('y','i') #old portuguese had y
	
	#problems related to Portugese language
	pdSeries = pdSeries.str.replace('za','sa') #Izabel x Isabel
	pdSeries = pdSeries.str.replace('zo','so') #Brazopolis x Braspolis
	pdSeries = pdSeries.str.replace('ze','se') #Euzebia x Eusebia
	pdSeries = pdSeries.str.replace('reo','reu') #poxoreu x poxoreo
	pdSeries = pdSeries.str.replace('tho','to') #thome x thome
	pdSeries = pdSeries.str.replace('tomaz','tomas') #thomaz x thomas
	pdSeries = pdSeries.str.replace('thi','ti') #with thiago x tiago
	pdSeries = pdSeries.str.replace('luiz','luis') #with luiz x luis
	pdSeries = pdSeries.str.replace('nea','nia') #with florinea x florinia

	#articles
	pdSeries = pdSeries.str.replace(' de ','dx')
	pdSeries = pdSeries.str.replace(' da ','dx')
	pdSeries = pdSeries.str.replace(' do ','dx')
	pdSeries = pdSeries.str.replace(' das ','dx')
	pdSeries = pdSeries.str.replace(' dos ','dx')

	#separator / and e
	pdSeries = pdSeries.str.replace('/','e')
	pdSeries = pdSeries.str.replace(' ','')

	return pdSeries

def removeLogFiles ():

	if path.exists("failFiles.txt"):
		remove("failFiles.txt") #remove failFiles if exists

	if path.exists("loadedFiles.txt"):
		remove("loadedFiles.txt") #remove loadedFiles if exists

	if path.exists("failedMun.txt"):
		remove("failedMun.txt") #remove failedMun if exists

	if path.exists("Prod_Municipal.csv"):
		remove("Prod_Municipal.csv") #remove failedMun if exists

