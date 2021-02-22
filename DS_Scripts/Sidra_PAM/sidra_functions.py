from pandas import DataFrame

def clean_csv (df):

	df = df.replace("...",0)
	df = df.replace("..",0)
	df = df.replace("-",0)
	df = df.dropna()

	dropNull = DataFrame(columns = ["Colum0"])
	
	dropNull["Colum0"] = df["Área Colhida"].astype(int) + df["Área Plantada"].astype(int)\
	+ df["Qtd.Produzida"].astype(int) + df["Valor Produção (Moeda em Real)"].astype(int)
	
	condition = DataFrame (columns = ["Cond"])
	condition["Cond"] = dropNull["Colum0"]==0
	conditionTrues = condition[condition["Cond"]==True]

	df = df.drop(conditionTrues.index)

	#Producion in thousand tons
	df["Qtd.Produzida"] = round(df["Qtd.Produzida"].astype(float)/1000,7)
	
	return df
