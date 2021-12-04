from gis_functions import *
import pandas as pd

data=pd.read_excel('half-way/steyr.xlsx')
print(data.PE)
x=get_nonitri_sum2(data)


print(x[['PE','no_nitri','PE_nonitri','%PE_no_nitri']])
print(x)