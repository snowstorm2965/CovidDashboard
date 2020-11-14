import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

import requests

DATA_URL = {
    "provincial": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv",
    "regional": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
    "national": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
    }

PROVINCES = pd.read_csv("./CovidDataPrep/data/list-of-provinces.csv")


def update_data_from_server(data_type="provincial"):
    # check if argument is in the list of URLs
    if data_type in DATA_URL:
        try:
            print("Downloading file %s ..." % DATA_URL[data_type])
            r = requests.get(DATA_URL[data_type])
            if r.ok:
                open("./CovidDataPrep/data/pcm-dpc/%s.csv" % data_type, "w").write(r.text)
        except Exception as ex:
            print("Exception caught: %s" % ex)
    else:
        # error
        print("Data type specified \"%s\" is unknown..." % data_type)

def generate_json_plots(data_type="provincial"):
    if data_type in DATA_URL:
        try:
            df = pd.read_csv("./CovidDataPrep/data/pcm-dpc/%s.csv" % data_type, encoding="ansi")
            if data_type == "provincial":
                for i, row in PROVINCES.iterrows():
                    if row['codice_provincia'] < 200:
                        idx = df['codice_provincia'] == row['codice_provincia']
                        data_toplot = df.loc[idx, ['data','totale_casi']]
                        data_toplot['variazione_totale_casi'] = np.concatenate((np.array([0]), np.diff(data_toplot['totale_casi'])))
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=data_toplot['data'],
                            y=data_toplot['totale_casi'],
                            line=dict(color="red"),
                            name="Total positive cases"
                            ))
                        fig.add_trace(go.Scatter(
                            x=data_toplot['data'],
                            y=data_toplot['variazione_totale_casi'],
                            line=dict(color="magenta"),
                            name="Variation"
                            ))
                        fig.update_layout(title="Data for %s (%s)"%(row['denominazione_provincia'],row['sigla_provincia']))
                        with open("./CovidDataPrep/data/json_plots/province_%s.json"%row['sigla_provincia'], "w") as out_file:
                            out_file.write('%s' % pio.to_json(fig,pretty=True))
        except Exception as ex:
            print("Exception caught: %s" % ex)
    else:
        # error
        print("Data type specified \"%s\" is unknown..." % data_type)

#df = pd.read_csv('coviddataprep/data/dpc-covid19-ita-province.csv')
#idx = df['sigla_provincia'] == 'to'
#fig = px.line(df[:][idx], x='data', y='totale_casi', title='to - totale casi', color='red')
#djson = pio.to_json(fig,pretty=true)
#with open('coviddataprep/data/dpc-covid19-ita-province-to.json', 'w') as out_file:
#    out_file.write('%s' % djson)