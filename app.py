from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func


engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Measurement= Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_twelve = '2016-08-23'
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>last_twelve).order_by(Measurement.date).all()
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.station, Station.name).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def stations():
    last_twelve = '2016-08-23'
    find_most_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()    
    top_station = find_most_active[0][0]
    last_twelve_monthtemps = session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.station == top_station).\
    filter(Measurement.date >= last_twelve).all()            
    return jsonify(last_twelve_monthtemps)


if __name__ == "__main__":
    app.run(debug=True)