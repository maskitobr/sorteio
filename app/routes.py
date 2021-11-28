import json
from flask import jsonify, render_template, redirect, url_for, request
from app import app
from .models import Results
from app.draw import draw, save_new_result


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", titulo="Sorteio Magnífico Mooca")


@app.route("/sortear/")
def run_draw():
    result = draw().all()
    return render_template("draw.html", titulo="Resultado", draw=result)


@app.route("/salvar", methods=["GET"])
def save():
    if request.method == "GET":
        save_new_result()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("run_draw"))


@app.route("/resultados/")
def show_results():
    results = app.session.query(Results).all()
    return render_template(
        "results.html", titulo="Histórico de Resultados", results=results
    )


@app.route("/resultados/<int:year>")
def by_year(year):
    load = app.session.query(Results).filter_by(year=year).first()
    result = json.loads(str(load.result).replace("'", '"'))
    return render_template(
        "year.html", titulo=f"Resultado {year}", result=result, year=year
    )


@app.route("/resultados/<int:year>/json")
def show_json_results(year):
    return jsonify(app.session.query(Results.result).filter_by(year=year).first())


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
