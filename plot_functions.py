
#import data and packages
import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from functions import *
from gis_functions import *

#prepare basemap for unified
#get separate boundaries of aech involved BL 

def get_boundaries(df):
    boundaries=[]
    #prepare basemaps
    basemap=geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    basemap.KG_NR=basemap.KG_NR.astype(int)
    basemap.to_crs(epsg=4326,inplace=True)

    for x in df.BL.unique():
        #isolate BL
        base =basemap[basemap.BL.isin([x]) ] # each BL needs own boundary. for BL in list isolate
        x=base.geometry.unary_union
        x=geopandas.GeoDataFrame(geometry=[x], crs=df.crs)
        boundaries.append(x)
        fig,ax=plt.subplots(1,figsize=(10,15))
        for x in boundaries:
            x.exterior.plot(edgecolor='k', linewidth=1, ax=ax)

#data=geopandas.read_file('final/export.geojson')


#do i actually need a function wrapppinh the already good plot tool? NO I DON'T
def plot(data, basemap, title, column, **kwargs):
    fig,ax=plt.subplots(1,figsize=(10,15))
    basemap.plot(ax=ax, alpha=0.3)
    ax.set_title(title, fontsize=15)
    data.plot(column=column, ax=ax, legend=True, scheme='equal_interval', k=10,
            legend_kwds=kwargs)
    plt.show()