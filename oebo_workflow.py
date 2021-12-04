#contains complete workflow for oebo


#import data and packages
import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from functions import *
from gis_functions import *

#import anlagedata
d='DATA/Sacken/Anlagendaten.xlsx'
data=pd.read_excel(d)
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
df=df[df.EW60<51]

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

#perform geo manipulations
joined=sjoin(gdf)

#extract data
extracted=extract_data_oebo(joined)

#reinsert 
final=final_merge_oebo(extracted)

#getting relative values
final['%nitri']=final.NITRIFIZIERUNG/final.freq*100
final['%no_nitri']=100-final['%nitri']
final['%before_reg']=final.before_reg/final.freq*100
final['no_nitri']=final.freq-final.NITRIFIZIERUNG

#standardize to general format
standard=final[['BKZ', 'BL', 'FL', 'GKZ', 'KG', 'KG_NR', 'before_reg', 'freq',
       'mean_year', 'sum_PE', 'geometry', '%before_reg',
       '%no_nitri']]

with open('final/oebo.geojson', 'w') as f:
    f.write(final.to_json())


##### col names for standardization to do
with open('standard/oebo.geojson', 'w') as f:
    f.write(standard.to_json())
