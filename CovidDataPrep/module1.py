import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.utils
import json

import requests

DATA_URL = {
    "provincial": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv",
    "regional": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
    "national": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
    }

provinces = pd.read_csv("./CovidDataPrep/data/list-of-provinces.csv")


def update_data_from_server(data_type="provincial"):
    # check if argument is in the list of URLs
    if data_type in DATA_URL:
        try:
            print("Downloading file %s ..." % DATA_URL[data_type])
            r = requests.get(DATA_URL[data_type])
            if r.ok:
                open("./CovidDataPrep/data/pcm-dpc/%s.csv" % data_type, "w", encoding="utf-8").write(r.text)
        except Exception as ex:
            print("Exception caught: %s" % ex)
    else:
        # error
        print("Data type specified \"%s\" is unknown..." % data_type)

def generate_json_plots(data_type="provincial"):
    if data_type in DATA_URL:
        try:
            df = pd.read_csv("./CovidDataPrep/data/pcm-dpc/%s.csv" % data_type)
            if data_type == "provincial":
                for i, row in provinces.iterrows():
                    if row['codice_provincia'] < 200:
                        idx = df['codice_provincia'] == row['codice_provincia']
                        data_toplot = df.loc[idx, ['data','totale_casi']]
                        data_toplot['nuovi_positivi'] = np.concatenate((np.array([0]), np.diff(data_toplot['totale_casi'])))
                        data_toplot.reset_index(inplace=True)
                        traces = [
                            dict(
                            x=data_toplot['data'],
                            y=data_toplot['totale_casi'],
                            name="Total positive cases",
                            line=dict(color="red"),
                            hovertemplate="%{y:d}"
                            ),
                            dict(
                            x=data_toplot['data'],
                            y=data_toplot['nuovi_positivi'],
                            name="New positive cases",
                            line=dict(color="magenta"),
                            hovertemplate="%{y:d}",
                            xaxis="x", yaxis="y2"
                            )
                            ]
                        layout = dict(grid=dict(rows=2,columns=1),
                                      title="Data for province %s (%s)"%(row['denominazione_provincia'],row['sigla_provincia']),
                                      showlegend=True
                                      )
                        latest = dict(total_cases=data_toplot.at[data_toplot.index[-1],'totale_casi'],
                                      new_cases=data_toplot.at[data_toplot.index[-1],'nuovi_positivi'],
                                      increasing=data_toplot.at[data_toplot.index[-1],'nuovi_positivi']>data_toplot.at[data_toplot.index[-2],'nuovi_positivi'])
                        data_tojson = dict(data_plot=traces, layout=layout, latest=latest)
                        with open("./CovidDataPrep/data/json_plots/province_%s.json"%row['sigla_provincia'], "w") as out_file:
                            out_file.write(json.dumps(data_tojson, cls=plotly.utils.PlotlyJSONEncoder))
        except Exception as ex:
            print("Exception caught: %s" % ex)
    else:
        # error
        print("Data type specified \"%s\" is unknown..." % data_type)