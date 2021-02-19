from flask import Flask, jsonify
from app import app
from .models import Units, Spaces


@app.route("/")
@app.route("/home")
def main():
    return f"This is the home page."


@app.route("/units/")
def show_units():
    unit_records = app.session.query(Units).all()
    return jsonify([unit.to_dict() for unit in unit_records])


@app.route("/spaces/")
def show_spaces():
    space_records = app.session.query(Spaces).all()
    return jsonify([space.to_dict() for space in space_records])


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
