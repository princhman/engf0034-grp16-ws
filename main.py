from flask import Flask, flash, redirect, render_template, request, session, url_for
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text
import sqlite3


app = Flask(__name__)
app.secret_key = "thisismysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)

@app.route("/")
def initial():
    return redirect(url_for("welcome"))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/stirring")
def stirring():
    return render_template("stirring.html")

@app.route("/temperature")
def temperature():
    return render_template("temperature.html")

@app.route("/ph")
def ph():
    return render_template("ph.html")


if __name__ == "__main__":
    app.run()
