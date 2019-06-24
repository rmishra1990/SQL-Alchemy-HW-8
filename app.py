from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
inspector = inspect(engine)


# function for precipitation for the last 12 months: 

def Precp_Year():
    myresult=engine.execute('SELECT date,prcp \
    FROM Measurement where DATETIME(date) < "2017-08-22" \
    AND DATETIME(date) > "2016-08-22" \
    ').fetchall()
    
    
    # Create a dictionary from the row data and append to a list
    res = []
    for result in myresult:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["prcp"] = result.prcp
        res.append(result_dict)

    return (res)

myres=Precp_Year()



#function for list of stations:

def all_stations(session):
    active_sta=session.query(Measurement.station, func.count(Measurement.tobs)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.tobs).desc()).all()
    #print(active_sta)
    return (active_sta)


# function for temperature for the last 12 months:

def Temp_year(engine):
    temp_all=engine.execute('SELECT station,date,tobs \
    FROM Measurement where DATETIME(date) < "2017-08-23" \
    AND DATETIME(date) > "2016-08-23" \
    ').fetchall()
    res = []
    for result in temp_all:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["station"] = result.station
        result_dict["tobs"] = result.tobs
        res.append(result_dict)
    return (res)

# function to calculate Tmin, Tavg, Tmax for start+end date:
def calc_temps(session,start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


# function to calculate Tmin, Tavg, Tmax for start date:
def calc_temp_start(session,start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()




### end of functions


app = Flask(__name__)


@app.route("/")
def home():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    var=Precp_Year()
    print(var)
    return  jsonify(var)



@app.route("/api/v1.0/stations")
def stations():
    var=all_stations(session)
    return jsonify(var)



@app.route("/api/v1.0/tobs")
def Temperature():
    var=Temp_year(engine)
    print(var)
    return jsonify(var)
    


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    var=calc_temps(session,start, end)
    return jsonify(var)


@app.route("/api/v1.0/<start>")
def start(start):
    var= calc_temp_start(session,start)
    return jsonify(var)


if __name__ == "__main__":
    app.run(debug=True)