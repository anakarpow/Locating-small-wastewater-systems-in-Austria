#merge pop file with geodata
#save geodata with gkz resolution


import pandas as pd
import numpy as np
import geopandas
import matplotlib.pyplot as plt
import os

#os.chdir('../')

#merge with basemap only
basemap=geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
pop=pd.read_excel('DATA/einwohnerzahl_1.1.2021_nach_gemeinden_mit_status_gebietsstand_1.1.2021.xlsx', header=1)
pop.rename(columns={'Gemeinde-kennziffer (GKZ)':'GKZ','Gemeindename':'PG','Bundesland':'BL','Bevölkerung\nam 1.1.2021':'Pop'},inplace=True)
pop.drop('Status',axis=1,inplace=True)
pop=pop.dropna(how='any')
"""GKZ=basemap.dissolve('GKZ')
gkz_pop=pd.merge(GKZ,pop, on='GKZ')
gkz_pop.plot(column='Pop')
gkz_pop.drop(columns=['MERIDIAN', 'BKZ', 'FA_NR', 'BL_KZ', 'ST_KZ','KG_NR', 'KG', 'PG_x',
                        'FA', 'GB_KZ', 'GB', 'VA_NR', 'VA', 'BL_x','ST','PG_y'],inplace=True)
gkz_pop.to_file('final/gkz_pop.gpkg', driver='GPKG')

"""


#merge with actual complete dataset
data=geopandas.read_file('final/complete.geojson')
gkz=data.dissolve('GKZ',aggfunc='sum')
gkz_pop=pd.merge(gkz,pop, on='GKZ')
gkz_pop.to_file('final/gkz_pop_new.gpkg', driver='GPKG')
#get values relative to POP
gkz_pop['%PEonpop']=gkz_pop.sum_PE_tot/gkz_pop.Pop*100
gkz_pop['%nonitriPEonpop']=gkz_pop.PE_nonitri_tot/gkz_pop.Pop*100
gkz_pop.to_file('final/gkz_pop+data.gpkg', driver='GPKG')
