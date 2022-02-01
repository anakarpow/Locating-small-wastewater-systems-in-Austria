import pandas as pd
import numpy as np
from functions import *
from gis_functions import extract_data_nospat, final_merge_nospat, join_nospat

d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA STMK NEU DE.xlsx'

data, trial = reader(d, 'Data Stmk', header=18, test=False)
data.dropna(how='all', axis=1,inplace=True)
data=cleaner(data,['Unnamed: 0', 'ID','Typ','Subtyp','Gewässer','Unnamed: 7','lfd.Nr.'])
no_geo=data[data.KG.isna()]
no_geo.to_excel('half-way/no_geo_steyr.xlsx', index=False)
#data=data[~data.KG.isna()] # AGGREAGTION TO gemeinde may be possible
#print(data[data.Jahr.isna()])  ###here we go 160 NAs
#####3

#some have wrong year. keep anyway. 
#data=data[data.Jahr>1700]
#print(len(data[data.Jahr<1700]))
#data.year=data.year.fillna(0)


data=data.fillna(0)
conditions_tech = [
    data["Unbek."] == 1,
    data["Mehr-kammer"] == 1,
    data["Durchl."] == 1, 
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

data=data.fillna(0)
data.PE=data.PE.astype(int)
data.KG_NR=data.KG_NR.astype(int)


data.to_excel('half-way/steyr.xlsx', index=False)


merged=join_nospat(data, 'steyr')

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



final=final_merge_nospat(total, 'steyr')

#data=data[data.PE<=50]

#merged=join_nospat(data, 'steyr_KKA')

#extracted=extract_data_nospat(merged)


#final=final_merge_nospat(extracted, 'steyr_KKA')