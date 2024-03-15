import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(autoload_with = engine)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
query_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).filter(Measurement.date <= func.date(recent_date)).all()

df = pd.DataFrame(results, columns=['Date', 'Precipitation'])
df['Precipitation'] = pd.to_numeric(df['Precipitation'], errors='coerce')
df = df.dropna().reset_index(drop = True)
df['Date'] = pd.to_datetime(df['Date'])

summary_of_statistics = pd.DataFrame(round(df['Precipitation'].describe(), 3))
sorted_data = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

stations = [item[0] for item in sorted_data]

most_active = sorted_data[0][0]
calc = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter_by(station = most_active).all()

data_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date >= query_date).filter(Measurement.date <= recent_date).all()

data_hist = pd.DataFrame(data_query, columns = ['Date', 'Temperature'])
data_hist['Temperature'] = pd.to_numeric(data_hist['Temperature'], errors = 'coerce')
data_hist = data_hist.dropna().reset_index(drop = True)




####################################################################################################
####################################################################################################
####################################################################################################
app = Flask(__name__)

@app.route('/')
def HomePage():
    return(
        'Available Routes:<br/>'
        '/api/v0.1/precipitation<br/>'
        '/api/v0.1/station<br/>'
        '/api/v0.1/tobs<br/>'
        '/api/v0.1/start/<start><br/>'
        '/api/v0.1/start/<start>/end/<end>')


@app.route('/api/v0.1/precipitation')
def get_precipitation_data():
    precipitation_dict = {}
    for result in results:
        precipitation_dict[result.date] = result.prcp
    return jsonify(precipitation_dict)


@app.route('/api/v0.1/station')
def get_station_data():
    station_dict = {}
    for i, station in enumerate(stations, start = 1):
        station_dict[i] = station
    return jsonify(station_dict)


@app.route('/api/v0.1/tobs')
def get_tobs_data():
    tobs_dict = {}
    for data in data_query:
        tobs_dict[data.date] = data.tobs
    return jsonify(tobs_dict)
 
    
# @app.route('/api/v0.1/start/<start>')
# def get_start_data(start):
#     try:
#         specified_date = dt.datetime.strptime(start, '%Y-%m-%d')
#     except ValueError:
#         return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

#     if specified_date > recent_date:
#         return jsonify({'error': 'Specified date is outside the valid range.'}), 400

#     calculated_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= specified_date).all()

#     if calculated_temp:
#         result_dict = {'TMIN': calculated_temp[0][0], 'TMAX': calculated_temp[0][1], 'TAVG': calculated_temp[0][2]}
#         return jsonify(result_dict)
#     else:
#         return jsonify({'error': 'Data not found for the specified date.'}), 404

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

    
if __name__ == '__main__':
    app.run(debug = True)