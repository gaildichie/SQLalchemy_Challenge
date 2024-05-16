# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

# GOt these from in structor
Last_Date = dt.datetime(2017, 8, 23)
One_Year_From_Last = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Routes:"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    return jsonify(stations=list(np.ravel(results)))



@app.route("/api/v1.0/tobs")
def tobs():
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_active_station = "USC00519281"
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date >= last_year_date).\
              filter(Measurement.station == most_active_station).all()
    tobs_data = [{"date": date, "temperature": tobs} for date, tobs in results]
    return jsonify(tobs_data)


#Got starter code for this route from instructor
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/")
@app.route("/api/v1.0/temp<start>/<end>")
def temp(start, end=None):
    start_date = dt.datetime.strptime(start, "%m%d%Y")
    if end is not None:
        end_date = dt.datetime.strptime(end, "%m%d%Y")
    else:
        end_date = Last_Date
    return f"{start_date}-{end_date}"    




if __name__ == "__main__":
    app.run(debug=True)






