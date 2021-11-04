from gis_functions import *


def prepare_oebo():
    d = 'C:/Users/fabrizio/Documents/repos/MSC/output/oebo.csv'
    gdf=csv_to_gdf(d)
    joined=sjoin(gdf)
    final=extract_data(joined)
    final.to_csv('final/oebo.csv',index=False)
    #final.to_file('output/oebo.shp')

def prepare_noe():
    d = 'C:/Users/fabrizio/Documents/repos/MSC/output/noe_geo.csv'
    gdf=csv_to_gdf(d)
    joined=sjoin(gdf)
    joined=extract_data(joined)
    joined.to_csv('final/noe.csv',index=False)
    #joined.to_file('output/noe.shp')


prepare_oebo()
prepare_noe()

def prepare_karn():
    d='output/Karn.xlsx'
    df=standard_form(d, 'KG_name','KG', 'Von', 'EW 60',
    'tech' ,'tech_type', missing_col=['type'])
    df.to_excel('final/Karn.xlsx',index=False)


def prepare_tirol():
    d='output/tirol.xlsx'
    df=standard_form(d, 'KG_name','KG','Von',
    'EW 60', 'bautyp','tech_type',missing_col=[])
    df.to_excel('final/tirol.xlsx',index=False)



def prepare_steyr():
    d='output/Steyr.xlsx'
    df=standard_form(d, 'KG_name','KG_NR','Jahr',
    'EW', 'bautyp','tech_type',missing_col=[])
    df.to_excel('final/steyr.xlsx',index=False)


def prepare_shape():
    df=prepare_steyr() #use output of function.xlsx
    joined=merge(df)
    joined=extract_data2(joined)
    #joined.plot()
    #plt.show()
    print(joined.columns)
    joined=joined[['BL','BKZ','GKZ','KG_NR','FL', 'freq','sum_EW','geometry']]

    joined.to_file('output/steyr.shp')