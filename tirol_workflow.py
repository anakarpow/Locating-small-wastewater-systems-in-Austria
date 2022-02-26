import pandas as pd
import numpy as np
from functions import *
import matplotlib.pyplot as plt
from  gis_functions import *

d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA Tirol NEU.xlsx'
data, trial = reader(d, 'Daten Tirol', header=18, test=False)

tech_type=data[[1, 2,3,  4,5,6,7,8,9,10,11,12,13]]
bautyp=data[['mech.','biol. ','chem.']]

conditions_tech = [
    data[1] == 1,
    data[2] == 1,
    data[3] == 1, 
    data[4] == 1,
    data[5] == 1,
    data[6] == 1,
    data[7] == 1,
    data[8] == 1,
    data[9] == 1,
    data[10] == 1,
    data[11] == 1,
    data[12] == 1,
    data[13] == 1,
]


outcome_tech = [ 'Primary', 'Bel.', 'SBR', 'MBR', 
                'Tropf','Rotation', 'Fest', 'Wirbel' ,
                'BKF', 'PKA','Primary', 'Kompost','Unbekannt']
data=logical_column(conditions_tech,outcome_tech,data,'tech_type')
conditions_bau = [
    data["mech."] == 'x',
    data["biol. "] == 'x',
    data["chem."] == 'x',
]

outcomes_bau = [
 "Mech", "Bio", "Chem"
]
data=logical_column(conditions_bau,outcomes_bau,data,'bautyp')

data=col_dropper(data,tech_type,bautyp)
data.dropna(how='all', axis=1,inplace=True)
data.dropna(how='all', axis=0,inplace=True)
#data=data.fillna(0)
data=cleaner(data,['Unnamed: 0','Urkunde','Lageplan','Anmerkungen','Unnamed: 35', 'KKA', 'Kl. KA', '?'])

data.rename(columns={'Unnamed: 5':'KG_name','Unnamed: 7':'tech_detail'},inplace=True)




data.rename(columns={'Unnamed: 5':'KG_name','Unnamed: 7':'tech_detail', 'Von':'year', 
'EW 60':'PE','KG':'KG_NR','KG_name':'KG'},inplace=True)

#400 have no PE
#data[data['EW 60']=='?']
#replace them now
data['PE']=data['PE'].replace('?', 0)

data['PE']=data['PE'].astype('str')
#data[data['EW 60'].str.contains('/', regex=False)]
#only one case. substitute
data['PE']=data['PE'].replace('?', '0')
data.PE=data.PE.replace(' ', 0)
data.loc[data.PE.str.contains('/'), 'PE']='0'
data['PE']=data['PE'].astype('float')

data['year']=data['year'].replace('?', '0')

data.year=data.year.astype(int)

#add column built before 1991
data['before_reg']=data.year<=1991
data['no_nitri']=data.tech_type=='Primary'


data.drop(columns=['Bis','m³/d', 'l/s', 'EW60 / m³/d','EW60 / l/s (10h)'], inplace=True)

data.to_excel('half-way/tirol.xlsx',index=False)

merged=join_nospat(data, 'tirol')

merged['design']=np.where(merged.PE<50, 'small','medium')
small=merged[merged.design=='small']
medium=merged[merged.design=='medium']

outlaw=medium[(medium.no_nitri==True)&(medium.year>1991)]

with open('half-way/outlaw_tirol.geojson', 'w') as f:
    f.write(outlaw.to_json())

small=extract_data_nospat(small)
medium=extract_data_nospat(medium)

total=small.merge(medium, on='KG_NR',how='outer',suffixes=('_small','_medium'))

total=total.fillna(0)
total['freq_tot']=total.freq_small+total.freq_medium
total['sum_PE_tot']=total.sum_PE_small+total.sum_PE_medium
total['no_nitri_tot']=total.no_nitri_small+total.no_nitri_medium
total['PE_nonitri_tot']=total.PE_nonitri_small+total.PE_nonitri_medium


final=final_merge_nospat(total, 'tirol')