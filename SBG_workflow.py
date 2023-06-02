import pandas as pd
import numpy as np
from functions import *
import matplotlib.pyplot as plt
from gis_functions import *

d = r'C:\Users\fabrizio\Documents\repos\MSC\DATA/KKA SBG NEU.xlsx'
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

outcome_tech = ['Primary', 'Andere','Andere', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 
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
data['no_nitri']=data.tech_type=='Primary'


data.to_excel('half-way/SBG.xlsx',index=False)


#lost 25 here
merged=join_nospat(data, 'SBG')

merged['design']=np.where(merged.PE<50, 'small','medium')
small=merged[merged.design=='small']
medium=merged[merged.design=='medium']
small=extract_data_nospat(small)
medium=extract_data_nospat(medium)

total=small.merge(medium, on='KG_NR',how='outer',suffixes=('_small','_medium'))

total=total.fillna(0)
total['freq_tot']=total.freq_small+total.freq_medium
total['sum_PE_tot']=total.sum_PE_small+total.sum_PE_medium
total['no_nitri_tot']=total.no_nitri_small+total.no_nitri_medium
total['PE_nonitri_tot']=total.PE_nonitri_small+total.PE_nonitri_medium


final=final_merge_nospat(total, 'SBG')
