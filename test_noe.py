#here the functions are tested and a file is produced. quality is fine

import pandas as pd
import numpy as np
from functions import *
import os


d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA NÖ NEU DE final.xlsx'

data, trial = reader(d, 'Data NÖ (Technol)', header=5, test=False)

# clean up
data = cleaner(data, ["Unnamed: 0", "Unnamed: 28",
               "Unnamed: 29", "Unnamed: 30"])
#data = data[data['EW60_BEWILLIGT'] < 51]

# change colnames
col_list = ['3-k', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 'Fest', 'Wirbel', 'BKF', 'PKA', 'Filtersack',
            'Kompost', 'Andere', 'Unbekannt']

data = change_colname_index(13, data, col_list)

# create subsets
bautyp = data[["Mechan.", "Biolog.", "Chemisch", "Unbek."]]
activity = data[["Betrieb", "Stillgelegt", "Unbek"]]
tech_type = data[col_list]


# work on bautyp
# check if slices have only one category
# bautyp has 8 issues
check_logic(bautyp)

# here we slice to the issues
# in fact, 8 rows have unbkenant and biologic
# for the moment put them to bio
issue = control_logic_issue(bautyp)

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

# work on tech_type

check_logic(tech_type)
control_logic_issue(tech_type)

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
    data["Filtersack"] == 1,
    data["Kompost"] == 1,
    data["Andere"] == 1,
]

outcome_tech = ['Unbekannt', '3-k', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 'Fest', 'Wirbel', 'BKF', 'PKA', 'Filtersack',
                'Kompost', 'Andere']

data = logical_column(conditions_tech, outcome_tech, data, 'tech_type')

# work on acitivity
check_logic(activity)
control_logic_issue(activity)

conditions_act = [
    data['Unbek'] == 1,
    data['Betrieb'] == 1,
    data['Stillgelegt'] == 1]

outcomes_act = ['Unbekannt', 'Betrieb', 'Stillgelegt']


data = logical_column(conditions_act, outcomes_act, data, 'activity')

# now drop all worked columns
data = col_dropper(data, activity, bautyp, tech_type)

os.chdir('output/')
data.to_csv('NOE.csv')
