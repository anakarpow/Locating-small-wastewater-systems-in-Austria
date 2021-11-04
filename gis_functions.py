import pandas as pd
import numpy as np
import geopandas
import matplotlib.pyplot as plt
from shapely import wkt


#workflow for data with coordinates
#reads csv file t gdf and prints plot to check projection
def csv_to_gdf(csv):
    df=pd.read_csv(csv)
    df['geometry']=df['geometry'].apply(wkt.loads)
    gdf = geopandas.GeoDataFrame(df, crs='WGS84')
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    austria=world[world['name']=='Austria']
    #gdf.plot(color='red', ax=austria.plot())
    #plt.show()
    print(gdf)
    return gdf

def sjoin(gdf):
    print('joining dataframes...')
    shp=geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    shp.KG_NR=shp.KG_NR.astype(int)
    shp.to_crs(epsg=4326,inplace=True)
    joined=geopandas.sjoin(shp, gdf, how='inner')

    #insert this in preprocessing
    #joined.INBETRIEBNAHME=joined.INBETRIEBNAHME.str.slice(0,4)
    #joined=joined[joined.INBETRIEBNAHME!='<NUL']
    #joined.INBETRIEBNAHME=joined.INBETRIEBNAHME.astype(int)

    return joined


def extract_data(joined):
    print('extracting data for gis')
    joined['freq'] = joined.groupby('KG_NR')['KG_NR'].transform('count')
    joined['sum_EW']=joined.groupby('KG_NR')['EW60'].transform('sum')
    joined['average_baujahr']=joined.groupby('KG_NR')['INBETRIEBNAHME'].transform('mean').astype(int)
    #joined=joined.drop_duplicates(subset='KG_NR')
    joined=joined[['BL','BKZ','GKZ','KG_NR','KG','FL', 'freq', 'sum_EW','average_baujahr','geometry']]
    return joined


def extract_data2(joined): #explicit for oebo
    print('extracting data for gis')
    joined['freq'] = joined.groupby('KG_NR')['KG_NR'].transform('count')
    joined['sum_EW']=joined.groupby('KG_NR')['EW60'].transform('sum')
    joined['average_baujahr']=joined.groupby('KG_NR')['INBETRIEBNAHME'].transform('mean').astype(int)
    #insert  %of only mechanic to freq

    joined=joined[['BL','BKZ','GKZ','KG_NR','KG','FL','geometry','ANLAGENAME', 'EW60', 'INBETRIEBNAHME',
       'VERFAHRENSART BIOLOGIE', 'REINIGUNG MECHANISCH', 'C-ENTFERNUNG',
       'NITRIFIZIERUNG', 'N-ENTFERNUNG', 'P-ENTFERNUNG', 'Tonne TM',
       'Verfahren', 'Typ', 'before_reg']]
    return joined

#workflow for data without coords

def standard_form(d,col_KG,col_KG_nr,col_date,col_EW,col_type,col_tech, missing_col):
    df=pd.read_excel(d)
    for x in missing_col:
        df[x]='tbd'
    df.rename(columns={col_KG:'KG',col_KG_nr:'KG_NR', col_date:'year',
                    col_EW:'EW60',col_type:'type',col_tech:'tech_type'},inplace=True)
    
    df=df[[ 'KG','KG_NR','year','EW60','type','tech_type']]
    df.replace({'?':0,'´':'', ' ':0}, inplace=True)
    df.fillna(0,inplace=True)
    df=df.astype({'KG':str,'KG_NR':int,'year':int,
                 'EW60':float,'type':str,
                 'tech_type':str})
    return df


def merge(df):
    shp=geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    shp.KG_NR=shp.KG_NR.astype(int)
    shp.to_crs(epsg=4326,inplace=True)
    joined=pd.merge(shp,df, on=['KG_NR'])
    return joined

def extract_data2(joined):
    print('extracting data for gis')
    joined['freq'] = joined.groupby('KG_NR')['KG_NR'].transform('count')
    joined['sum_EW']=joined.groupby('KG_NR')['EW60'].transform('sum')
    #joined['average_baujahr']=joined.groupby('KG_NR')['Jahr'].transform('mean').astype(int)
    joined=joined.drop_duplicates(subset='KG_NR')
    #joined=joined[['KG_NR', 'KG', 'freq', 'sum_EW','average_baujahr','geometry']]
    return joined

#newt steps
#finish workflow for non-spatial datasets
#-add cols with coutn of techtype?
#-how to visualize beyirk, gemeinde, staatsgrenze?

#prio unify function fo spatial data

#unify all finished datasets 
#play on gis 