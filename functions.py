#this file contains the cleaning functions

import pandas as pd
import numpy as np


def reader(file, sheetname, header, test=False):
    data = pd.read_excel(file, sheet_name=sheetname, header=header)
    if test == True:
        print(data.head())
        print(data.columns)
    trial = data.head(100)
    return data, trial


def cleaner(df, col_drop):
    df = df.dropna(how="all", axis=0)
    df = df.drop(col_drop, axis=1)
    return df


def change_colname_index(start, df, col_list):
    count = start
    for name in col_list:
        df.columns.values[count] = name
        count = count+1
    return df


'''
the workflow could be 
1 check_logic for consisntency. needs subsets
2 if pos then logical_column. needs conditions and outcomes
3 test_logical_column to see for errors. here improvent can be made, how to simplify func?
4 if pos col_dropper with subsets from step 1
'''

# this function sums the rows of subsets.
# because categories are marked with 1s, each row suh only sum up to 1
# any other case is sketchy
# return a sum of trues compared to len of df
# pass multiple subsets of df possible


def check_logic(*args):
    for x in args:
        check = x.sum(axis=1) == 1
        test = check.value_counts()
        print('')
        print(
            '          result of logical check: which rows have only one category?'.upper())
        print(test)
        #print(f" values ==1 :", test, "on total {len(x)}")
    return test, len(x)

# what happens when not all rows sum up to 1?
# first, see which rows are problem
# this is fine, it returns rows but with new index. fine for now
# when multiple args are passed, only last one is returned. should save to list or similar
# test passed


def control_logic_issue(*args):
    for x in args:
        df = x[0:0]
        issue_row = x[x.sum(axis=1) != 1]
        df = df.append(issue_row)
        print('')
        print(
            '            result of control_issues: identify rows with multiple categories'.upper())
        print(df)
    return df


# this function creates a new column summarizing categorical columns
def logical_column(conditions, outcomes, df, colname, test=False):
    if test == True:
        copy = df
        copy[colname] = np.select(conditions, outcomes)
        return copy[colname]
    else:
        df[colname] = np.select(conditions, outcomes)
    return df

# this function compares the new column with original.
# returns empty list if all went good


def test_logical_column(series, string1, df, col1, string2, col2):
    a = series == string1
    b = df[col1] == 1
    c = series == string2
    d = df[col2] == 1
    test1 = a.compare(b)
    test2 = c.compare(d)
    return test1, test2


# rebuild col dropper to use subsets
def col_dropper(df, *args):
    for x in args:
        col_drop = list(x.columns)
        df = df.drop(col_drop, axis=1)
    return df

# dropping by slices


def col_dropper_slice(start, stop, df, test=False):
    col_drop = list(range(start, stop))
    if test == True:
        exp = df.drop(df.columns[col_drop], axis=1)
        return exp
    df = df.drop(df.columns[col_drop], axis=1)


#def unify_halfway(df):
    



''''
SUBSETS
bautyp=trial[["Mechan.", "Biolog.", "Chemisch", "Unbek."]]
activity=trial[["Betrieb","Stillgelegt","Unbek"]]
tech_type=trial.iloc[:,13:27]




VARIABLES

#bautyp
conditions=[
    trial["Unbek."]==1,
    trial["Mechan."]==1,
    trial["Biolog."]==1,
    trial["Chemisch"]==1,
    (trial["Biolog."]==1) & (trial["Mechan."]==1)
    ]

outcomes=[
    "Unbekannt","Mech","Bio","Chem","Bio"
]

#tech_type
tech_type["Unbekannt"]==1,
tech_type["3-k"]==1,
tech_type["Bel."]==1,
tech_type["SBR"]==1,
tech_type["MBR"]==1,
tech_type["Tropf"]==1,
tech_type["RBC"]==1,
tech_type["Fest"]==1,
tech_type["Wirbel"]==1,
tech_type["BKF"]==1,
tech_type["PKA"]==1,
tech_type["Filtersack"]==1,
tech_type["Kompost"]==1,
tech_type["Andere"]==1,
]


outcome=['Unbekannt','3-k', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 'Fest', 'Wirbel','BKF','PKA', 'Filtersack',
        'Kompost', 'Andere']






'''
