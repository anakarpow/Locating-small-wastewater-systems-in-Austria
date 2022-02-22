#contains complete workflow for oebo
# -*- coding: utf-8 -*-

#import data and packages
import geopandas as geopandas
import pandas as pd
import matplotlib.pyplot as plt
from functions import *
from gis_functions import *

#import anlagedata
d='DATA/Sacken/Anlagendaten.xlsx'
data=pd.read_excel(d)
no_geo=data[data.Longitude.isna()]
no_geo.to_excel('half-way/no_geo_oebo.xlsx',index=False)
data=data.dropna(how='any', subset= ['Longitude'])

#create geometry from coordinates 
#only studying the geometry of the shp made possible to intepret this file correctly
gdf=geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy((data['Longitude']), data['KOORDX(GK M31)'], crs='EPSG:31258'))

#take onlty <50
#anlage=gdf[gdf.EGW<51]
anlage=gdf
anlage.dropna(how='all',inplace=True)

anlage.loc[anlage.Bundesnummer.astype(str).str.contains('-'), 'Bundesnummer']='0'
anlage.loc[anlage.Bundesnummer.astype(str).str.contains('_'), 'Bundesnummer']='0'




#import dataset with wrong coords but technical features
d = 'C:/Users/fabrizio/Documents/repos/MSC/DATA/Sacken/raw_data.xlsx'
df=pd.read_excel(d, sheet_name='Rohdaten ARA 500 EW')
df=df[df.EW60<=500]

#prepare for merge
anlage=anlage.astype({'Bundesnummer':'int'})
df.rename(columns={'BUNDESNUMMER':'Bundesnummer'}, inplace=True)

#merge
merged=pd.merge(df, anlage, on='Bundesnummer')
merged.dropna(subset=['Longitude','KOORDX(GK M31)_y'],inplace=True)

#get a geodf
gdf=geopandas.GeoDataFrame(merged, geometry=geopandas.points_from_xy((merged['Longitude']), merged['KOORDX(GK M31)_y'], crs='EPSG:31258'))

#change coordinate system
gdf.to_crs(epsg=4326,inplace=True)

#drop columns with <80% real data, not NA.
gdf=gdf[gdf.columns[gdf.isnull().mean()<0.8]]

#drop unused geodata
gdf=gdf.drop(columns=['KOORDX(GK M31)_y', 'Latitude','KOORDY(GK M31)_y','Longitude','GRUPPE', 'FABRIKATTYPE','ABLEITUNG IN','KOORDX(GK M31)_x', 'KOORDY(GK M31)_x'])

#format year columns. show only year
gdf.INBETRIEBNAHME=gdf.INBETRIEBNAHME.astype('str')
gdf.INBETRIEBNAHME=gdf.INBETRIEBNAHME.str.split('-').str[0]
gdf.INBETRIEBNAHME=gdf.INBETRIEBNAHME.str.split(',').str[0]
gdf=gdf[gdf.INBETRIEBNAHME!='<NULL>']
gdf.INBETRIEBNAHME=gdf.INBETRIEBNAHME.astype(int)

#format columns
gdf.Verfahren=gdf.Verfahren.str.strip(' ')

#drop columns
gdf.drop(columns=['Bundesnummer', 'ANLAGETEILNAME','Realisierungsstatus',
'KOORDINATEN GENAUIGKEIT', 'WASSERBUCH','dtKläranlage','Größenklasse',
'Kommunal/Industriell', 'EGW', 'BEZIRK'],inplace=True)
gdf.Verfahren=gdf.Verfahren.str.strip(' ')

#add column built before 1991
gdf['before_reg']=gdf.INBETRIEBNAHME<=1991

#replace with bool values for further analisys
gdf.replace({'j':True,'n':False}, inplace=True)



gdf.to_excel('half-way/oebo.xlsx', index=False)
gdf.to_file('half-way/oebo.gpkg', driver='GPKG')

#perform geo manipulations
joined=sjoin(gdf, 'oebo')

joined['design']=np.where(joined.EW60<50, 'small','medium')
small=joined[joined.design=='small']
medium=joined[joined.design=='medium']

small=extract_data_oebo(small)
medium=extract_data_oebo(medium)

total=small.merge(medium, on='KG_NR',how='outer',suffixes=('_small','_medium'))

print(total)
print(total.columns)

total=total.fillna(0)
total['freq_tot']=total.freq_small+total.freq_medium
total['sum_PE_tot']=total.sum_PE_small+total.sum_PE_medium
total['nitri_tot']=total.NITRIFIZIERUNG_small+total.NITRIFIZIERUNG_medium
total['no_nitri_tot']=total.freq_tot-total.nitri_tot
total['PE_nonitri_tot']=total.PE_nonitri_small+total.PE_nonitri_medium
total=total.fillna(0)

print(total)
print(total.columns)



#reinsert 
final=final_merge_oebo(total, 'oebo')

print(final)
print(final.columns)

"""#standardize to general format
standard=final[['BKZ', 'BL', 'FL', 'GKZ', 'KG', 'KG_NR', 'before_reg', 'freq',
       'mean_year', 'sum_PE', 'geometry', '%before_reg',
       '%no_nitri']]

with open('final/oebo.geojson', 'w') as f:
    f.write(final.to_json())


##### col names for standardization to do
with open('standard/oebo.geojson', 'w') as f:
    f.write(standard.to_json())
"""