from flask import Flask, jsonify, render_template, redirect, url_for, request
from app import app
from .models import Units, Slots, Results
from app.funcs import *
from app.draw import *


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', titulo='Sorteio Magnífico Mooca')


@app.route("/sortear/", methods=['GET', 'POST'])
def run_draw():
    result = draw().all()
    return render_template('draw.html', titulo='Resultado', draw=result)


@app.route("/resultados/", methods=['GET'])
def show_results():
    results = app.session.query(Results).all()
    return render_template('results.html', titulo='Histórico de Resultados', results=results)


@app.route("/resultados/<int:year>", methods=['GET'])
def by_year(year):
    result = app.session.query(Results).filter_by(year=year).first()
    load = json.loads(str(result.result).replace("'", '"'))
    return render_template('year.html', titulo=f'Resultado {year}', result=load, year=year)


"""
@app.route("/results/json")
def show_json_results():
    return jsonify([i.serialize for i in app.session.query(Units).order_by(Units.dual).all()])
"""


@ app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
