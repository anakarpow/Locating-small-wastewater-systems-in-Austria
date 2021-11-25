import pandas as pd
import numpy as np
from functions import *
import matplotlib.pyplot as plt
from gis_functions import *

d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA Kärnten NEU.xlsx'

data, trial = reader(d, 'Data K', header=15, test=False)


data=cleaner(data, ['Unnamed: 0','Unnamed: 1','Unnamed: 8','Bautyp','mech.','biol. ','chem.','Urkunde','Von.1','Lageplan','Anmerkungen',1,2,3,4,5,6,7,8,9,10,11,12,13,'Unnamed: 35','KKA','Kl. KA','?','Unnamed: 38'])
data.dropna(how='all', inplace=True, axis=0, thresh=10)
conditions_tech=[
    data['Kat.'] == 1,
    data['Kat.'] == 2,
    data['Kat.']== 3,
    data['Kat.'] == 4,
    data['Kat.'] == 5,
    data['Kat.'] == 6,
    data['Kat.'] == 7,
    data['Kat.']== 8,
    data['Kat.']== 9,
    data['Kat.']== 10,
    data['Kat.']== 11,
    data['Kat.']== 12,
    data['Kat.']== 13
]

outcome_tech = ['3-k', 'Filtersack','Kompost', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 
                    'Fest', 'Wirbel', 'BKF', 'PKA','Unbekannt']
data=logical_column(conditions_tech, outcome_tech, data,'tech_type')
data.rename(columns={'Unnamed: 6':'KG','Von':'year', 
'EW 60':'PE','KG':'KG_NR'},inplace=True)


data['PE']=data['PE'].replace('?', 0)

data['year']=data['year'].astype('str')
#data[data['year'].str.contains('/')]
data.loc[data.year.str.contains('/'), 'year']='0'
data.loc[data.year.str.contains('´1974'), 'year']='1974'
data.loc[data.year.str.contains('´1966'), 'year']='1966'



data.year=data.year.replace("´", "")
data['year']=data['year'].replace('?', '0')



#add column built before 1991
data.year=data.year.astype(int)

data['before_reg']=data.year<=1991
data['no_nitri']=data.tech_type=='3-k'


data.to_excel('half-way/Karn.xlsx',index=False)

#about 130 have no KG
no_ref=data[data.KG.isna()]
no_ref.to_excel('half-way/no_geo_karn.xlsx', index=False)

data.KG_NR.fillna(0,inplace=True)
data.KG.fillna(0,inplace=True)




merged=join_nospat(data)

extracted=extract_data_nospat(merged)


final=final_merge_nospat(extracted, 'Karn')