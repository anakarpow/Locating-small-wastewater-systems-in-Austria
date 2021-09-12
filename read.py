import pandas as pd
import json

d = r'C:/Users/fabrizio/Documents/R_data/PROJECTS/MASTER/DATA/KKA NÖ NEU DE final.xlsx'


def reader(file, test=False):
    data = pd.read_excel(file, sheet_name='Data NÖ (Technol)', header=5)
    if test == True:
        print(data.head())
        print(data.columns)
    trial = data.head(100)
    return data, trial


reader(d)

# get dict with index and headers


def headers(trial):
    original = trial.columns
    config = {}
    col_nr = 0
    with open("config_col1.json", 'w') as foo:
        for x in original:
            config[x] = str(x).title()
        json.dump(config, foo)
        foo.close()


def headers_list(trial):
    with open('headers.txt', 'w') as foo:
        for col in trial.columns:
            foo.write(str(col).title()+"\n")
    foo.close()


final = ['3-k', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 'Fest', 'Worbel', 'PKA', 'Filtersack',
         'Kompost', 'Andere', 'Unbekannt']


def headers_add():
    with open('headers.txt', 'a') as foo:
        for x in final:
            x = "\n"+x
            foo.writelines(x)
    foo.close()


# struggling!
# function to change headers feeding upper
# translate tech type
# translate bio, mech
final = ['3-k', 'Bel.', 'SBR', 'MBR', 'Tropf', 'RBC', 'Fest', 'Worbel', 'PKA', 'Filtersack',
         'Kompost', 'Andere', 'Unbekannt']


def reshape(trial):
    trial.drop(["Unnamed: 28", "Unnamed: 29", "Unnamed: 30"], axis=1)
    print(trial.columns)

    with open("headers.txt", "r") as foo:
        headers = []
        for x in foo.readlines():
            x = x.strip("\n")
            headers.append(x)
    trial.columns = headers
    print(trial.columns)


def reshape2(trial):
    trial = pd.DataFrame(trial)
    trial.rename(columns={1: "porcoddio"}, inplace=True)
    print(trial.columns)


def main(d):
    data, trial = reader(d)
    reshape(trial)


main(d)
