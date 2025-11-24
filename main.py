import sqlite3
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text

from graphs import *
from mqtt import init_accumulator, on_message

app = Flask(__name__)
app.secret_key = "thisismysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)


db = SQLAlchemy(app)


class Stirring(db.Model):
    stirring_id = db.Column("stirring_id", db.Integer, primary_key=True)
    stirring_speed = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __init__(self, stirring_speed, timestamp):
        self.stirring_speed = stirring_speed
        self.timestamp = timestamp

    def get_stirring_id(self):
        return self.stirring_id

    def get_stirring_speed(self):
        return self.stirring_speed

    def get_timestamp(self):
        return self.timestamp


class Temperature(db.Model):
    temperature_id = db.Column("temperature_id", db.Integer, primary_key=True)
    temperature_level = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __init__(self, temperature_level, timestamp):
        self.temperature_level = temperature_level
        self.timestamp = timestamp

    def get_temperature_id(self):
        return self.temperature_id

    def get_temperature_level(self):
        return self.temperature_level

    def get_timestamp(self):
        return self.timestamp


class PH(db.Model):
    ph_id = db.Column("ph_id", db.Integer, primary_key=True)
    ph_level = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __init__(self, ph_level, timestamp):
        self.ph_level = ph_level
        self.timestamp = timestamp

    def get_ph_id(self):
        return self.ph_id

    def get_ph_level(self):
        return self.ph_level

    def get_timestamp(self):
        return self.timestamp


@app.route("/")
def initial():
    return redirect(url_for("welcome"))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/stirring", methods=["GET", "POST"])
def stirring():
    if request.method == "POST":
        stirring_speed = request.form["stirring_speed"]
        current_datetime = datetime.now()
        # add_stirring_speed = Stirring(stirring_speed, current_datetime)
        # db.session.add(add_stirring_speed)
        # db.session.commit()
        return redirect(url_for("stirring"))
    else:
        return render_template("stirring.html")


@app.route("/temperature")
def temperature():
    if request.method == "POST":
        temperature_level = request.form["temperature_level"]
        current_datetime = datetime.now()
        # add_temperature_level = Temperature(temperature_level, current_datetime)
        # db.session.add(add_temperature_level)
        # db.session.commit()
        return redirect(url_for("temperature"))
    else:
        return render_template("temperature.html")


@app.route("/ph")
def ph():
    if request.method == "POST":
        ph_level = request.form["ph_level"]
        current_datetime = datetime.now()
        # add_ph_level = PH(ph_level, current_datetime)
        # db.session.add(add_ph_level)
        # db.session.commit()
        return redirect(url_for("ph"))
    else:
        return render_template("ph.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Initialize the accumulator with database and models
        init_accumulator(
            db,
            {
                "PH": PH,
                "Temperature": Temperature,
                "Stirring": Stirring,
                "datetime": datetime,
            },
        )
    client.loop_start()
    app.run()
