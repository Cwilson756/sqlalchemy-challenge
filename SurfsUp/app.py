import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta


# Database Setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the tables
measurement = Base.classes.measurement
station = Base.classes.station

# Create the session
session = Session(engine)

# Flask Setup

app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
     f"<h2>Here are the available routes:</h2>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query to retrieve the last 12 months of precipitation data and return the results."""    
   
    #create database link
    session = Session(engine)
    
    #calculate one year ago date
    last_measurement = session.query(
        measurement.date).order_by(measurement.date.desc()).first()
    (latest_date, ) = last_measurement
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    latest_date = latest_date.date()
    one_year = latest_date - relativedelta(years=1)
    
    # query precipitation score from the past year
    one_year_data = session.query(measurement.date, measurement.prcp).filter(
        measurement.date >= one_year).all()
    
    session.close()
    
    all_precipication = []
    for date, prcp in one_year_data:
        if prcp != None:
            prcp_dict = {}
            prcp_dict[date] = prcp
            all_precipication.append(prcp_dict)

    return jsonify(all_precipication)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # create session
    session = Session(engine)

    # query for the stations
    stations = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()

    session.close()

    # convert results to dictionary
    station_list = []
    for station, name, latitude, longitude, elevation in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_list.append(station_dict)

    # jsonify stations dict
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query for the dates and temperature observations from a year from the last data point for the most active station."""
    # create session
    session = Session(engine)

    # calculate the date one year ago (from most current data point)
    last_measurement = session.query(
        measurement.date).order_by(measurement.date.desc()).first()
    (latest_date, ) = last_measurement
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    latest_date = latest_date.date()
    date_year_ago = latest_date - relativedelta(years=1)

    # find the most active station
    most_active_station = session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count().desc()).\
        first()

    # get the most active station ID
    (most_active_station_id, ) = most_active_station
    print(
        f"The station id of the most active station is {most_active_station_id}.")

    #  querry date and temp data from the most active station over the one year period
    last_year_data = session.query(measurement.date, measurement.tobs).filter(
        measurement.station == most_active_station_id).filter(measurement.date >= date_year_ago).all()

    session.close()

    # convert querry results to dictionary
    temp_list = []
    for date, temp in last_year_data:
        if temp != None:
            temp_dict = {}
            temp_dict[date] = temp
            temp_list.append(temp_dict)
    # return the JSONified dict
    return jsonify(temp_list)

@app.route('/api/v1.0/<start>', defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")
def temps():
    """Return a JSON list of the average, minimum, and maximum temperature for a given start or start-end range."""
    """When given the start only, calculate the average, minimum, and maximum temperature for all dates greater than and equal to the start date."""
    """When given the start and the end date, calculate the average, minimum, and maximum temperature for dates between the start and end date inclusive."""
    # create session
    session = Session(engine)

    # with both start and end date
    if end != None:
        temp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).filter(
            measurement.date <= end).all()
    # with only start date
    else:
        temp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

    session.close()

    # convert results to list
    temperature_list = []
    no_temperature_data = False
    for min_temp, avg_temp, max_temp in temp_data:
        if min_temp == None or avg_temp == None or max_temp == None:
            no_temperature_data = True
        temperature_list.append(min_temp)
        temperature_list.append(avg_temp)
        temperature_list.append(max_temp)
    # jsonify the dict
    if no_temperature_data == True:
        return f"No temperature data found for the given date range. Try another date range."
    else:
        return jsonify(temperature_list)


if __name__ == '__main__':
    app.run(debug=True)