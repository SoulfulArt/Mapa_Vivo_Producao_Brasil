#These are functions and variables that support script loadCSV.py

from os import remove
from os import path

#function that organizes numerical data because some files use , as thousand
#separator or , as decimal separator

def simplifyNumber (df):
	
	df["Producao"] = df["Producao"].astype(str).str.replace(',','.')
	df["AreaH"] = df["AreaH"].astype(str).str.replace(',','.')
	df["Valor"] = df["Valor"].astype(str).str.replace(',','.')

	df["Producao"] = df["Producao"].astype(float)
	df["AreaH"] = df["AreaH"].astype(float)
	df["Valor"] = df["Valor"].astype(float)
	
	#Rendimento is a function of producao and area
	df["Rendimento"] = (df["Producao"]/df["AreaH"])
	df["Rendimento"] = round(df["Rendimento"],2)

	return df

'''Function that replace letter with accent for letter without accent it can generate
problems in finding cities that are the same but has different accents from the
datasets. Other transformations that are specific of the data that is used in this
project such as '/' for ' e ' were identified as an important substituion to help
data manipulation through the project.'''

def simplifyText (pdSeries):
	
	#it's better to work with homogenous casing
	pdSeries = pdSeries.str.lower()
	
	#cities that have name changes
	pdSeries = pdSeries.str.replace('fortaleza do tabocão','tabocão')
	pdSeries = pdSeries.str.replace('augusto severo','campo grande')	
	

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
	pdSeries = pdSeries.str.replace('thi','ti') #thiago x tiago
	pdSeries = pdSeries.str.replace('luiz','luis') #luiz x luis
	pdSeries = pdSeries.str.replace('florinea','florinia') #florinea x florinia
	pdSeries = pdSeries.str.replace(' moz',' mos') # moz x mos (porto)
	pdSeries = pdSeries.str.replace(' luz',' lus') # santa luz x lus
	pdSeries = pdSeries.str.replace('cruz','crus') #vera cruz x crus
	pdSeries = pdSeries.str.replace('das artes','') #embu das artes x embu
	pdSeries = pdSeries.str.replace('terezinha','teresinha') #terezinha x teresinha
	
	#articles
	pdSeries = pdSeries.str.replace(' de ','dx')
	pdSeries = pdSeries.str.replace(' da ','dx')
	pdSeries = pdSeries.str.replace(' do ','dx')
	pdSeries = pdSeries.str.replace(' das ','dx')
	pdSeries = pdSeries.str.replace(' dos ','dx')

	#separator / and e
	pdSeries = pdSeries.str.replace('/','e')
	pdSeries = pdSeries.str.replace(' ','')
	
	#some cities are comming with state initials
	pdSeries = pdSeries.str.replace('(ac)','', regex = False)
	pdSeries = pdSeries.str.replace('(al)','', regex = False)
	pdSeries = pdSeries.str.replace('(ap)','', regex = False)
	pdSeries = pdSeries.str.replace('(am)','', regex = False)
	pdSeries = pdSeries.str.replace('(ba)','', regex = False)
	pdSeries = pdSeries.str.replace('(ce)','', regex = False)
	pdSeries = pdSeries.str.replace('(df)','', regex = False)
	pdSeries = pdSeries.str.replace('(es)','', regex = False)
	pdSeries = pdSeries.str.replace('(go)','', regex = False)
	pdSeries = pdSeries.str.replace('(ma)','', regex = False)
	pdSeries = pdSeries.str.replace('(mt)','', regex = False)
	pdSeries = pdSeries.str.replace('(ms)','', regex = False)
	pdSeries = pdSeries.str.replace('(mg)','', regex = False)
	pdSeries = pdSeries.str.replace('(pa)','', regex = False)
	pdSeries = pdSeries.str.replace('(pb)','', regex = False)
	pdSeries = pdSeries.str.replace('(pr)','', regex = False)
	pdSeries = pdSeries.str.replace('(pe)','', regex = False)
	pdSeries = pdSeries.str.replace('(pi)','', regex = False)
	pdSeries = pdSeries.str.replace('(rj)','', regex = False)
	pdSeries = pdSeries.str.replace('(rg)','', regex = False)
	pdSeries = pdSeries.str.replace('(rn)','', regex = False)
	pdSeries = pdSeries.str.replace('(rs)','', regex = False)
	pdSeries = pdSeries.str.replace('(ro)','', regex = False)
	pdSeries = pdSeries.str.replace('(rr)','', regex = False)
	pdSeries = pdSeries.str.replace('(sc)','', regex = False)
	pdSeries = pdSeries.str.replace('(sp)','', regex = False)
	pdSeries = pdSeries.str.replace('(se)','', regex = False)
	pdSeries = pdSeries.str.replace('(to)','', regex = False)
			
	return pdSeries
		
#Function cleanDataCSV clens data from a DataFrame

def cleanDataCSV (df):
		
		#Valor Produção (Moeda em Real) must have number values
		df = df[df['Valor Produção (Moeda em Real)']!='...']
		df = df[df['Valor Produção (Moeda em Real)']!='..']
		df = df[df['Valor Produção (Moeda em Real)']!='-']
		df = df[df['Nome Lavoura']!='Total']
		
		#Qtd.Produzida can't be NaN, but Valor can
		df = df[df["Qtd.Produzida"].notna()]
				
		df = df.reset_index(drop = True)
		
		return df
