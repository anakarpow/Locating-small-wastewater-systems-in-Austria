# here are function for spatial preparation

from geopandas.base import GeoPandasBase
import pandas as pd
import numpy as np
import geopandas
import matplotlib.pyplot as plt
from shapely import wkt





#######################################################
#SPATIAL ROUTINE
#######################################################


#POINTS GEOMETRY
def file_to_gdf(file,control=False):
#reads csv file t gdf and prints plot to check projection
    try:
        df = pd.read_csv(file)
    except:
        df = pd.read_excel(file)

    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = geopandas.GeoDataFrame(df, geometry='geometry', crs='WGS84')
    if control==True:
        world = geopandas.read_file(
            geopandas.datasets.get_path('naturalearth_lowres'))
        austria = world[world['name'] == 'Austria']
        gdf.plot(color='red', ax=austria.plot())
        plt.show()
    return gdf



def sjoin(gdf):
    """
    spatial join for point geometries
    return gdf 

    """
    print('joining dataframes...')
    shp = geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    shp.KG_NR = shp.KG_NR.astype(int)
    shp.to_crs(epsg=4326, inplace=True)
    joined = geopandas.sjoin(shp, gdf, how='inner')
    print('done')

    # insert this in preprocessing
    # joined.INBETRIEBNAHME=joined.INBETRIEBNAHME.str.slice(0,4)
    # joined=joined[joined.INBETRIEBNAHME!='<NUL']
    # joined.INBETRIEBNAHME=joined.INBETRIEBNAHME.astype(int)

    return joined

#################################################
#OEBO ROUTINE
def extract_data_oebo(joined):
    """
    return df with one row per KG
    only summary columns like sum EW,  average values and so on

    insert column for each Tech_type sum ? like sum_SBR=5
    """
    df1=joined.groupby(['KG_NR','KG']).agg(lambda row: np.count_nonzero(row)).reset_index()
    df2=joined.groupby(['KG_NR','KG']).sum().reset_index().loc[:,['KG_NR','EW60','Tonne TM']]
    df3=joined.groupby(['KG_NR','KG']).mean().astype(int).reset_index().loc[:,['KG_NR','INBETRIEBNAHME']]
    merged=pd.merge(df2,df3, on='KG_NR')
    extracted=df1.merge(merged,on='KG_NR')
    extracted.rename(columns={'EW60_y':'sum_PE','Tonne TM_y':'sum_TM(t)','INBETRIEBNAHME_y':'mean_year','MERIDIAN':'freq' },inplace=True)
    extracted=extracted[['KG_NR','freq', 'REINIGUNG MECHANISCH', 'C-ENTFERNUNG',
    'NITRIFIZIERUNG', 'N-ENTFERNUNG', 'P-ENTFERNUNG', 'before_reg', 'sum_PE','sum_TM(t)','mean_year']]
    print(extracted)
    extracted=get_nonitri_sum2(extracted)
    print(extracted)

    return extracted

def final_merge_oebo(extracted):
    """
    return geojson with one row per KG
    contains geoinformation and ready to plot

    """

    shp = geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    shp.KG_NR = shp.KG_NR.astype(int)
    shp.to_crs(epsg=4326, inplace=True)
    final=pd.merge(shp,extracted, on='KG_NR')


    print(final.geometry.is_valid.value_counts())
    final=final[['BL', 'BKZ', 'GKZ', 'KG_NR', 'KG', 'FL', 'geometry','freq', 'REINIGUNG MECHANISCH', 'C-ENTFERNUNG',
       'NITRIFIZIERUNG', 'N-ENTFERNUNG', 'P-ENTFERNUNG', 'before_reg',
       'sum_PE', 'sum_TM(t)', 'mean_year','%PE_no_nitri','sum_PE_nonitri' ]]
    with open('final/oebo.geojson', 'w') as f:
        f.write(final.to_json())
    return final

#################################################
#NOE ROUTINE
def extract_data_noe(joined):
    """
    return df with one row per KG
    only summary columns like sum EW,  average values and so on

    insert column for each Tech_type sum ? like sum_SBR=5
    """
    df1=joined.groupby(['KG_NR','KG']).agg(lambda row: np.count_nonzero(row)).reset_index()
    df2=joined.groupby(['KG_NR','KG']).sum().reset_index().loc[:,['KG_NR','EW60']]
    try:
        df3=joined.groupby(['KG_NR','KG']).mean().astype(int).reset_index().loc[:,['KG_NR','INBETRIEBNAHME']]
    except:
        df3=joined.groupby(['KG_NR','KG']).mean().reset_index().loc[:,['KG_NR','INBETRIEBNAHME']].astype(int)
    merged=pd.merge(df2,df3, on='KG_NR')
    extracted=df1.merge(merged,on='KG_NR')
    extracted.rename(columns={'EW60_y':'sum_PE','INBETRIEBNAHME_y':'mean_year','MERIDIAN':'freq' },inplace=True)
    extracted=extracted[['KG_NR','freq','before_reg', 'sum_PE','mean_year', 'no_nitri']]
    extracted=get_nonitri_sum2(extracted)
    return extracted

def final_merge_noe(extracted):
    """
    return geojson with one row per KG
    contains geoinformation and ready to plot

    """

    shp = geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    shp.KG_NR = shp.KG_NR.astype(int)
    shp.to_crs(epsg=4326, inplace=True)
    final=pd.merge(shp,extracted, on='KG_NR')

    print(final.geometry.is_valid.value_counts())
    #getting relative values
    final['%before_reg']=final.before_reg/final.freq*100
    final['%no_nitri']=final.no_nitri/final.freq*100

    with open('final/noe.geojson', 'w') as f:
        f.write(final.to_json())
    return final



# workflow for data without coords


def standard_form(d, col_KG, col_KG_nr, col_date, col_EW, col_type, col_tech, missing_col):
    df = pd.read_excel(d)
    for x in missing_col:
        df[x] = 'tbd'
    df.rename(columns={col_KG: 'KG', col_KG_nr: 'KG_NR', col_date: 'year',
                       col_EW: 'EW60', col_type: 'type', col_tech: 'tech_type'}, inplace=True)

    df = df[['KG', 'KG_NR', 'year', 'EW60', 'type', 'tech_type']]
    df.replace({'?': 0, '´': '', ' ': 0}, inplace=True)
    df.fillna(0, inplace=True)
    df = df.astype({'KG': str, 'KG_NR': int, 'year': int,
                    'EW60': float, 'type': str,
                   'tech_type': str})
    return df




########################################################
#NON-SPATIAL ROUTINE
########################################################

def join_nospat(df):
    shp = geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    shp.KG_NR = shp.KG_NR.astype(int)
    shp.to_crs(epsg=4326, inplace=True)
    merged=pd.merge(shp, df, on='KG_NR')
    if len(df[~df.KG_NR.isin(merged.KG_NR)]) ==0:
        print('perfect merge')
    else:
        print('not all rows have been merged')
        not_merged=df[~df.KG_NR.isin(merged.KG_NR)]
        not_merged.to_excel('final/not_merged.xlsx')
    print()

    return merged

def extract_data_nospat(joined):
    """
    return df with one row per KG
    only summary columns like sum EW,  average values and so on

    insert column for each Tech_type sum ? like sum_SBR=5
    """
    #PE_nonitri=get_nonitri_sum2(joined)

    df1=joined.groupby(['KG_NR']).agg(lambda row: np.count_nonzero(row)).reset_index()
    df2=joined.groupby(['KG_NR']).sum().reset_index().loc[:,['KG_NR','PE']]
    try:
        df3=joined.groupby(['KG_NR']).mean().astype(int).reset_index().loc[:,['KG_NR','year']]
    except :
        df3=joined.groupby(['KG_NR']).mean().reset_index().loc[:,['KG_NR','year']].astype(int)

    merged=pd.merge(df2,df3, on='KG_NR')
    extracted=df1.merge(merged,on='KG_NR')
    extracted.rename(columns={'PE_y':'sum_PE','year_y':'mean_year','MERIDIAN':'freq' },inplace=True)
    extracted=extracted[['KG_NR','freq','before_reg', 'sum_PE','mean_year', 'no_nitri']]
    #extracted.join(PE_nonitri, on='KG_NR')

    return extracted

def final_merge_nospat(extracted, BL_name):
    """
    return geojson with one row per KG
    contains geoinformation and ready to plot

    """

    shp = geopandas.read_file('DATA/shp_new/Oesterreich_BEV_VGD_LAM.shp')
    shp.KG_NR = shp.KG_NR.astype(int)
    shp.to_crs(epsg=4326, inplace=True)
    final=pd.merge(shp,extracted, on='KG_NR')

    print(final.geometry.is_valid.value_counts())

    #getting relative values
    final['%no_nitri']=final.no_nitri/final.freq*100
    final['%before_reg']=final.before_reg/final.freq*100

    #`final=standardize_format(final)

    with open('final/' + BL_name +'.geojson', 'w') as f:
        f.write(final.to_json())
    return final

#######################################################
#UNIFYING ROUTINE
#######################################################

def standardize_format(df):
    df=df[['BL', 'BKZ', 'GKZ', 'KG_NR', 'KG', 'FL', 'geometry','freq', 'before_reg',
       'sum_PE', 'mean_year', 'no_nitri', '%no_nitri','%before_reg']]


# newt steps
# finish workflow for non-spatial datasets
# -add cols with coutn of techtype?

# prio unify functions

# unify all finished datasets


def get_nonitri_sum(df):
    try:
        print(len(df))
        x=df.groupby(['KG_NR','no_nitri']).sum().reset_index()
        y=x.loc[x['no_nitri']==True]
        print(len(y))
    except:
        x=df.groupby(['KG_NR','NITRIFIZIERUNG']).sum().reset_index()
        y=x.loc[x['NITRIFIZIERUNG']==False]

    try:
        y=y[['KG_NR','PE']]
        y.rename(columns={'PE':'sum_PE_nonitri'}, inplace=True)
    except:
        y=y[['KG_NR','EW60']]
        y.rename(columns={'EW60':'sum_PE_nonitri'}, inplace=True)     
    return y

def insert_nonitri_sum(no_nitri_sum, df):
    print(len(df))
    data=pd.merge(df,no_nitri_sum,on='KG_NR')
    print(len(no_nitri_sum))
    print(len(data))
    data['%PE_no_nitri']=(data.sum_PE_nonitri/data.sum_PE)*100
    return data


def get_nonitri_sum2(df):
    def cond(df):
        try:
            if df['no_nitri']==True:
                return df['PE']
            else:
                return 0
                
        except:
            if df['NITRIFIZIERUNG']==False:
                return df['sum_PE']
            else:
                return 0


    PE_nonitri=df.apply(cond, axis=1)

    return PE_nonitri
    try:
        df['%PE_no_nitri']=(df.PE_nonitri/df.PE)*100
    except:
        df['%PE_no_nitri']=(df.PE_nonitri/df.EW60)*100


    return df



"""
try:
        df['PE_nonitri']=df.apply(lambda row: print(row['PE']) )
        df['%PE_no_nitri']=(df.PE_nonitri/df.sum_PE)*100
    except:
        df['PE_nonitri']=df.apply(df.PE if df.NITRIFIZIERUNG==False else 0 )
        df['%PE_no_nitri']=(df.PE_nonitri/df.sum_PE)*100

"""