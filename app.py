import pandas as pd
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Setting up database

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Setting up Flask
app = Flask(__name__)

# Flask Routes

@app.route("/")
def home():
    return (
        f"Available Route:<br/>"
        f"/api/v1.0/precipitation<br/>"
    )

@app.route("/api/v1.0/precipitation/")
def precipitation():

    # Calculate the date one year from the last date in data set.
    last12months = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    dataprecipscores = dict(session.query(measurement.date, measurement.prcp).filter(measurement.date >= last12months).order_by(measurement.date).all())

    return jsonify(dataprecipscores)

if __name__ == "__main__":
    app.run(debug=True)