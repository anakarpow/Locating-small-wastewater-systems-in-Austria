#here the csv from oebo_real is read and projected
import pandas as pd
import numpy as np
import geopandas
import matplotlib.pyplot as plt
from shapely import wkt


d = 'C:/Users/fabrizio/Documents/repos/MSC/output/oebo.csv'

df=pd.read_csv(d)


df['geometry'] = df['geometry'].apply(wkt.loads) #read geometry column
gdf = geopandas.GeoDataFrame(df, crs='WGS84')

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
austria=world[world['name']=='Austria']

gdf.plot(color='red', ax=austria.plot())
plt.show()


# gdf=geopandas.points_from_xy(data['geometry'], crs='WGS84')
