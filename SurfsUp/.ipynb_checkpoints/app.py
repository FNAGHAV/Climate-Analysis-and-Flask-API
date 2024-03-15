
# import warnings
# warnings.filterwarnings('ignore')
import os
os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"]="1"
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)

result = Base.classes.keys()
print(result)

# Save reference to the table
# Measurement = Base.classes.measurement
# Session = Base.classess.session


#################################################
# Flask Setup
#################################################
# app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

# @app.route("/")
# def Homepage():
#     """List all available api routes"""
#     return (
#         f"Available Routes:<br />"
#         f"/api/v1.0/precipitation<br />"
#         f"/api/v1.0/stations<br />"
#         f"/api/v1.0/tobs<br />"
        
#     )


# @app.route("/api/v1.0/precipitation")
# def Precipitation():
#     query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#     session = Session(engine)
#     recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
#     results = session.query(Measurement.date, Measurement.prcp).\
#             filter (Measurement.date >= query_date).filter (Measurement.date <= recent_date).all()
#     session.close()
#     precipitation_data = {}
#     for date, prcp in results:
#         precipitation_data[date] = prcp

#     return jsonify(precipitation_data)


# if __name__ == '__main__':
#     app.run(debug=True)
