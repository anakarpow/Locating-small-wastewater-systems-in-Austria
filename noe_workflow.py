#unifying workflow file for NOE

#needs more comments
#need more data extraction

#non-nitrifying plants 

#import data and packages
import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from functions import *
from gis_functions import *

d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA NÖ NEU DE final.xlsx'

data, trial = reader(d, 'Data NÖ (Technol)', header=5, test=False)

data = cleaner(data, ["Unnamed: 0", "Unnamed: 28",
               "Unnamed: 29", "Unnamed: 30"])

#work on bautyp
bautyp = data[["Mechan.", "Biolog.", "Chemisch", "Unbek."]]
conditions_bau = [
    data["Unbek."] == 1,
    data["Mechan."] == 1,
    data["Biolog."] == 1,
    data["Chemisch"] == 1,
    (data["Biolog."] == 1) & (data["Mechan."] == 1)
]

outcomes_bau = [
    "Unbekannt", "Mech", "Bio", "Chem", "Bio"
]

data = logical_column(conditions_bau, outcomes_bau, data, 'bautyp')
data=col_dropper(data, bautyp)
data

#work on tech_type
col_list = ['3-k', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 'Fest', 'Wirbel', 'BKF', 'PKA', 'Filtersack',
         'Kompost', 'Andere', 'Unbekannt']



change_colname_index(9, data,col_list)
conditions_tech = [
    data["Unbekannt"] == 1,
    data["3-k"] == 1,
    data["Bel."] == 1,
    data["SBR"] == 1,
    data["MBR"] == 1,
    data["Tropf"] == 1,
    data["RBC"] == 1,
    data["Fest"] == 1,
    data["Wirbel"] == 1,
    data["BKF"] == 1,
    data["PKA"] == 1,
    data["PKA"] == '1',
    data["Filtersack"] == 1,
    data["Kompost"] == 1,
    data["Andere"] == 1,
]


outcome_tech = ['Unbekannt','3-k', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 'Fest', 'Wirbel', 'BKF', 'PKA','PKA', 'Filtersack',
                'Kompost', 'Andere']

#
data=logical_column(conditions_tech,outcome_tech, data, 'tech_type' )
data=col_dropper(data, data[col_list] )
activity = data[["Betrieb", "Stillgelegt", "Unbek"]]
check_logic(activity)

#
conditions_act=[
    data['Unbek']==1,
    data['Betrieb']==1,
    data['Stillgelegt']==1]

outcomes_act=['Unbekannt', 'Betrieb','Stillgelegt']


#
data=logical_column(conditions_act, outcomes_act,data, 'activity')
data=col_dropper(data, activity)


#add column built before 1991
data['before_reg']=data.BEWILLIGUNGSJAHR<=1991
data['no_nitri']=data.bautyp=='Mech'



data.rename(columns={'EW60_BEWILLIGT':'EW60','BEWILLIGUNGSJAHR':'INBETRIEBNAHME'},inplace=True)


no_geo=data[data.RECHTSWERT.isna()]
no_type=data[data.tech_type=='Unbekannt']

#print out esxcel. needs column dropping
data.to_excel('half-way/noe.xlsx',index=True)

#anyway in halfway
#no_geo.to_excel('half-way/no_geo_noe.xlsx')
no_type.to_excel('half-way/no_type_noe.xlsx')



#get gdf. this combi is the correct one
gdf=geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy((data['RECHTSWERT']), data['HOCHWERT'], crs='GKM34'))
#gdf.drop(columns=['Unnamed: 0', 'Unnamed: 0.1','RECHTSWERT', 'HOCHWERT', ],inplace=True)
gdf.to_crs(epsg=4326,inplace=True)
gdf.rename(columns={'EW60_BEWILLIGT':'EW60','BEWILLIGUNGSJAHR':'INBETRIEBNAHME'},inplace=True)


#perform geo manipulations
joined=sjoin(gdf, 'noe')


extracted=extract_data_noe(joined)

print(extracted)

final=final_merge_noe(extracted, 'noe')


gdf=gdf[gdf.EW60<=50]

#perform geo manipulations
joined=sjoin(gdf, 'noe')
extracted=extract_data_noe(joined)
final=final_merge_noe(extracted, 'noe_KKA')



#with open('standard/noe.geojson', 'w') as f:
 #   f.write(final.to_json())


#to do
#check standardize format function. why not workin g?








#data.to_csv('half-way/NOE.csv', index=False)