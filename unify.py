
#import data and packages
import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from functions import *
from gis_functions import *


oebo=geopandas.read_file('standard/oebo.geojson')
noe=geopandas.read_file('final/noe.geojson')

df_list=[oebo,noe]

unify=pd.concat(df_list)