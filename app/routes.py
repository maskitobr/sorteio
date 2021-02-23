from flask import Flask, jsonify
from app import app
from .models import Units, Spaces


@app.route("/")
@app.route("/home")
def main():
    return f"This is the home page."


@app.route("/results/")
def show_results():
    return jsonify([i.serialize for i in app.session.query(Units).order_by(Units.dual).all()])


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
