# Import the dependencies
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Create an engine to connect to the SQLite database 
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

#Reflect the database tables
Base = automap_base()
Base.prepare(autoload_with = engine)

# Create references to the Measurement and Station tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session object to interact with the database
session = Session(engine)

# Calculate the date one year ago from the last data point in the database
recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
query_date = dt.date(2017,8,23) - dt.timedelta(days = 365)

# Query for the dates and precipitation values
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).filter(Measurement.date <= func.date(recent_date)).all()

# summary_of_statistics = pd.DataFrame(round(df['Precipitation'].describe(), 3))

# Query for the temperature observations of the most active station for the previous year
sorted_data = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

stations = [item[0] for item in sorted_data]
most_active = sorted_data[0][0]
calc = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter_by(station = most_active).all()

# Query for temperature statistics for dates greater than or equal to the specified start date
data_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date >= query_date).filter(Measurement.date <= recent_date).all()


#################################################
# Flask Setup
#################################################
# Initialize the Flask application
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define the homepage route
@app.route('/')
def HomePage():
    return(
        'Available Routes:<br/>'
        '/api/v0.1/precipitation<br/>'
        '/api/v0.1/station<br/>'
        '/api/v0.1/tobs<br/>'
        '/api/v0.1/start/<start><br/>'
        '/api/v0.1/start/<start>/end/<end>')

# Define the precipitation route
@app.route('/api/v0.1/precipitation')
def get_precipitation_data():
    precipitation_dict = {}
    for result in results:
        precipitation_dict[result.date] = result.prcp
    return jsonify(precipitation_dict)

# Define the stations route
@app.route('/api/v0.1/station')
def get_station_data():
    station_dict = {}
    for i, station in enumerate(stations, start = 1):
        station_dict[i] = station
    return jsonify(station_dict)

# Define the temperature observations route
@app.route('/api/v0.1/tobs')
def get_tobs_data():
    tobs_dict = {}
    for data in data_query:
        tobs_dict[data.date] = data.tobs
    return jsonify(tobs_dict)
 
# Define the route for start date temperature statistics    
@app.route('/api/v0.1/start/<start>')
def get_start_data(start):
    try:
        specified_date = dt.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    # Proceed with querying the database for temperature data
    calculated_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= specified_date).all()

    if calculated_temp:
        
        ave_temp = round(calculated_temp[0][2], 1)
        result_dict ={'TMIN': calculated_temp[0][0], 'TMAX': calculated_temp[0][1], 'TAVG': calculated_temp[0][2]}
    
        return jsonify(result_dict)
    else:
        return jsonify({'error': 'Data not found for the specified date.'}), 404
    

# Define the route for start and end date temperature statistics  
@app.route('/api/v0.1/start/<start>/end/<end>')
def get_start_end_data(start, end):
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    calculated_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    if calculated_temp:
        
        avg_temp = round(calculated_temp[0][2], 1)

        result_dict ={'TMIN': calculated_temp[0][0], 'TMAX': calculated_temp[0][1], 'TAVG': calculated_temp[0][2]}
        return jsonify(result_dict)
    else:
        return jsonify({'error': 'Data not found for the specified date range.'}), 404

# Run the Flask application    
if __name__ == '__main__':
    app.run(debug = True)