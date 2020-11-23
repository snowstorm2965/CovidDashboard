"""
Routes and views for the flask application.
"""
from flask import render_template, jsonify, request, Response
from CovidDashboard import app
import json
import pandas as pd

df = pd.read_csv("./CovidDataPrep/data/list-of-provinces.csv")
regions = df[['codice_regione','denominazione_regione']].drop_duplicates().copy()
regions.reset_index(inplace=True,drop=True)
#provinces = df[df.codice_provincia<200][['codice_regione','codice_provincia','denominazione_provincia','sigla_provincia']].copy()
provinces = df[df.codice_provincia<200].copy()


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        regions_list = regions,
        selected_region_index = 0,
        provinces_list = provinces[provinces.codice_regione==regions.codice_regione[0]],
        selected_province_index = 0
    )

@app.route('/list_regions')
def list_region():
    return Response(regions.to_json(orient="records"), mimetype='application/json')

@app.route('/list_provinces')
def list_provinces():
    selected_region_code = int(request.args['selected_region_code'])
    #result = provinces[provinces.codice_regione==selected_region_code][['codice_provincia','denominazione_provincia','sigla_provincia']]
    result = provinces[provinces.codice_regione==selected_region_code]
    if not(result.empty):
        return Response(result.to_json(orient="records"), mimetype='application/json')

@app.route('/plot_province', methods=["GET"])
def plot_province():
    try:
        selected_province_code = int(request.args['selected_province_code'])
        selected_region_code = int(request.args['selected_region_code'])
        result = provinces[(provinces.codice_provincia==selected_province_code) & (provinces.codice_regione==selected_region_code)]
        if len(result.index) == 1:
                with open("./CovidDataPrep/data/json_plots/province_%s.json" % result.sigla_provincia.iloc[0], "r") as read_file:
                    data = json.load(read_file)
                    return data
        else:
            print("bad province code")
    except Exception as ex:
        print("Exception while trying to get province plot: %s" % ex)


