"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify, request
from CovidDashboard import app
import json

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/plot_province', methods=["GET"])
def plot_province():
    selected_province = request.args['selected']
    try:
        with open("./CovidDataPrep/data/json_plots/province_%s.json"%selected_province, "r") as read_file:
            data = json.load(read_file)
            # print(type(data))
            return data
    except Exception as ex:
        print("Exception while trying to get province plot: %s" % ex)
