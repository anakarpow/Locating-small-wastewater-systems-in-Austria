import pandas as pd
import numpy as np
from functions import *
import matplotlib.pyplot as plt
from gis_functions import *

d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA SBG NEU.xlsx'
data, trial = reader(d, 'Daten SBG', header=11, test=False)
conditions_tech=[
    data['Kat'] == 1,
    data['Kat'] == 2,
    data['Kat']== 3,
    data['Kat'] == 4,
    data['Kat'] == 5,
    data['Kat'] == 6,
    data['Kat'] == 7,
    data['Kat']== 8,
    data['Kat']== 9,
    data['Kat']== 10,
    data['Kat']== 11,
    data['Kat']== 12,
    data['Kat']== 13
]

outcome_tech = ['3-k', 'Filtersack','Kompost', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 
                    'Fest', 'Wirbel', 'BKF', 'PKA','Unbekannt']

data=logical_column(conditions_tech,outcome_tech,data, 'tech_type')
drop_col=[ 'Unnamed: 0','Unnamed: 1','Unnamed: 8','mech.','biol. ',
'chem.','Urkunde','Unnamed: 13','Lageplan','Bautyp', 'Anmerkungen','Kat',
1,2,3,4,5,6,7,8,9,10,11,12,13,'12.1','Bepflanzter Bodenfilter (Pflanzenkläranlage)']



data=cleaner(data,drop_col)
data.rename(columns={'Unnamed: 6':'KG_name'},inplace=True)
data.replace({'?':'0'},inplace=True)
data.fillna(0,inplace=True)

data.rename(columns={'Von':'year', 'EW 60':'PE', 'KG':'KG_NR','KG_name':'KG'},inplace=True)
data=data.drop(columns=['Bis'])
data.PE=data.PE.replace(' ', 0).astype(float)
data.year=data.year.astype(int)

data['before_reg']=data.year==1991
data['no_nitri']=data.tech_type=='3-k'


data.to_excel('half-way/SBG.xlsx',index=False)

#sum_nonitri=get_nonitri_sum(data)

merged=join_nospat(data)

extracted=extract_data_nospat(merged)


#extracted=insert_nonitri_sum(sum_nonitri,extracted)

final=final_merge_nospat(extracted, 'SBG')
