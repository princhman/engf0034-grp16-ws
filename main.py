import sqlite3
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text

from graphs import *
from mqtt import *

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
        on_set("stirring", stirring_speed)

        return redirect(url_for("stirring"))
    else:
        now = datetime.now()
        time_list = []
        for time in range(7):
            time_calculated = (now - timedelta(seconds=time*10))
            time_list.append(time_calculated)

        data_points = []
        for value in range(6):
            time_mean = (Stirring.query.with_entities(func.avg(Stirring.stirring_speed)).filter(Stirring.timestamp <= time_list[value]).filter(Stirring.timestamp > time_list[value + 1]).scalar())
            data_points.append(time_mean)

        date_value_list = generate_lists(time_list, data_points)
        graphJSON = stirring_graph(date_value_list)
        refresh_graphs()
        return render_template("stirring.html", graphJSON=graphJSON)


@app.route("/temperature", methods=["GET", "POST"])
def temperature():
    if request.method == "POST":
        if "ChangeTimeFrame" in request.form:
            time_frame = request.form["time_frame"]
        elif "EditParameter" in request.form:
            temperature_level = request.form["temperature_level"]
            current_datetime = datetime.now()
            try:
                temperature_level = int(temperature_level)
            except:
                #flash("please input an integer for temperature level")
                return redirect(url_for("temperature"))
            #flash("temperature level successfully submitted")
            on_set("temperature", temperature_level)
        # add_temperature_level = Temperature(temperature_level, current_datetime)
        # db.session.add(add_temperature_level)
        # db.session.commit()
        return redirect(url_for("temperature"))
    else:
        now = datetime.now()
        time_list = []
        for time in range(7):
            time_calculated = (now - timedelta(seconds=time*10))
            time_list.append(time_calculated)

        data_points = []
        for value in range(6):
            time_mean = (Temperature.query.with_entities(func.avg(Temperature.temperature_level)).filter(Temperature.timestamp <= time_list[value]).filter(Temperature.timestamp > time_list[value + 1]).scalar())
            data_points.append(time_mean)

        date_value_list = generate_lists(time_list, data_points)
        graphJSON = temperature_graph(date_value_list)
        refresh_graphs()
        return render_template("temperature.html", graphJSON=graphJSON)


@app.route("/ph", methods=["GET", "POST"])
def ph():
    if request.method == "POST":
        ph_level = request.form["ph_level"]
        current_datetime = datetime.now()
        try:
            ph_level = int(ph_level)
        except:
            #flash("please input an integer for ph level")
            return redirect(url_for("ph"))
        on_set("ph", ph_level)
        #flash("ph level successfully submitted")
        return redirect(url_for("ph"))
    else:
        now = datetime.now()
        time_list = []
        for time in range(7):
            time_calculated = (now - timedelta(seconds=time*10))
            time_list.append(time_calculated)

        data_points = []
        for value in range(6):
            time_mean = (PH.query.with_entities(func.avg(PH.ph_level)).filter(PH.timestamp <= time_list[value]).filter(PH.timestamp > time_list[value + 1]).scalar())
            data_points.append(float(time_mean) if time_mean is not None else None)

        date_value_list = generate_lists(time_list, data_points)
        graphJSON = ph_graph(date_value_list)
        refresh_graphs()
        return render_template("ph.html", graphJSON=graphJSON)

def generate_lists(time_list, data_points):
    date_value_list = []
    '''if graph_type == "stirring":
        query = Stirring.query.limit(100).all()
        value_attr = "stirring_speed"
    elif graph_type == "temperature":
        query = Temperature.query.limit(100).all()
        value_attr = "temperature_level"
    elif graph_type == "ph":
        query = PH.query.limit(100).all()
        value_attr = "ph_level"'''
    for x in range (6):
        format_date_time = time_list[x].strftime("%Y-%m-%d %H:%M:%S")
        date_value_list.append([format_date_time, data_points[x]])
    print(date_value_list)
    return date_value_list

def refresh_graphs():
    now = datetime.now()
    one_day_ago = (now - timedelta(days=1))
    ph_query = PH.query.filter(PH.timestamp<=one_day_ago)
    for query in ph_query:
        db.session.delete(query)
        db.session.commit()


    # delete everything 24 hours ago

    #if ph
    

    # last minute
    # calculate mean of data within 10 secs
    # for all data within 10 secs - add up and divide by count
    # add data to graph

    # last hour
    # calculate mean of data within 10 minutes
    # for all data within 10 minutes - add up and divide by count
    # add data to graph

    # last day
    # calculate mean of data within 10 minutes
    # for all data within 10 minutes - add up and divide by count
    # add data to graph


    # display graph based on time frame


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