import pandas as pd
import numpy as np
from functions import *
from gis_functions import extract_data_nospat, final_merge_nospat, join_nospat

d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA STMK NEU DE.xlsx'

data, trial = reader(d, 'Data Stmk', header=18, test=False)
data.dropna(how='all', axis=1,inplace=True)
data=cleaner(data,['Unnamed: 0', 'ID','Typ','Subtyp','Gewässer','Unnamed: 7','lfd.Nr.'])

data=data[~data.KG.isna()]
print(data[data.Jahr.isna()])  ###here we go 160 NAs
#####3
#just for now -deleting NA in years because it destroys mean. which meybe is irrelevant anyway
data=data[data.Jahr>1700]



data=data.fillna(0)
conditions_tech = [
    data["Unbek."] == 1,
    data["Mehr-kammer"] == 1,
    data["Durchl."] == 1, #
    data["SBR"] == 1,
    data["MBR"] == 1,
    data["Tropf"] == 1,
    data["Fest"] == 1,
    data["BKF"] == 1,
    data["PKA"] == 1,
    data["Tauch"] == 1,
    data["Andere"] == 1,
]


outcome_tech = ['Unbekannt', '3-k', 'Bel.', 'SBR', 'MBR', 
                'Tropf', 'Fest',  'BKF', 'PKA',
                'Tauch', 'Andere']



data=logical_column(conditions_tech,outcome_tech,data,'tech_type')
conditions_bau = [
    data["Unbek."] == 1,
    data["Mechan."] == 1,
    data["Biolog"] == 1,
    data["Andere"] == 1,
    (data["Biolog"] == 1) & (data["Mechan."] == 1)
]

outcomes_bau = [
    "Unbekannt", "Mech", "Bio", "Andere", "Bio"
]
data=logical_column(conditions_bau,outcomes_bau,data,'bautyp')
tech_type=data[['Mehr-kammer', 'Durchl.',
       'SBR', 'MBR', 'Tropf', 'Tauch', 'Fest', 'PKA', 'BKF']]


bautyp=data[['Mechan.', 'Biolog', 'Andere', 'Unbek.',]]
data=col_dropper(data,tech_type,bautyp)

data['KG_NR']=data.KG.str.split().str[0]
data['KG_name']=data.KG.str.split().str[1]
data.drop(columns=['KG'],inplace=True)


#add column built before 1991. should build function 
data['before_reg']=data.Jahr<=1991
data['no_nitri']=data.bautyp=='Mech'
data.rename(columns={'KG_name':'KG', 'EW':'PE', 'Jahr':'year'}, inplace=True)
data.PE.replace(' ',0, inplace=True)  #about 1000 rows are 0 for column PE
data.PE=data.PE.astype(int)
data.KG_NR=data.KG_NR.astype(int)


data.to_excel('half-way/steyr.xlsx', index=False)


merged=join_nospat(data)

extracted=extract_data_nospat(merged)


final=final_merge_nospat(extracted, 'steyr')