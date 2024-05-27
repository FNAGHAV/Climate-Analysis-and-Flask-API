# Climate Analysis and Flask API

Background:
In this project, a climate analysis was conducted on a specific area using Python and SQLAlchemy. The analysis involved exploring climate data stored in a SQLite database named hawaii.sqlite. The subsequent sections outline the steps taken to accomplish this task.

Part 1: Analyze and Explore the Climate Data

In this section, the following steps were completed:

Connection to Database:
The SQLAlchemy create_engine() function was used to establish a connection to the SQLite database.

Reflect Tables:
The SQLAlchemy automap_base() function was utilized to reflect the tables into classes named 'station' and 'measurement'.

Create Session:
A SQLAlchemy session was created to link Python to the database.

Precipitation Analysis:

The most recent date in the dataset was identified.
The previous 12 months of precipitation data were queried.
The query results were loaded into a Pandas DataFrame and sorted by date.
The precipitation data were plotted using Matplotlib.
Summary statistics for the precipitation data were printed using Pandas.

Station Analysis:

A query was designed to calculate the total number of stations in the dataset.
The most-active stations were identified based on observation counts.
A query was designed to calculate the lowest, highest, and average temperatures for the most-active station.
The previous 12 months of temperature observation (TOBS) data for the most-active station were queried and plotted as a histogram.

Part 2: Design Your Climate App

In this section, a Flask API was designed based on the queries developed in the previous analysis. The following routes were created:

Homepage (/):

Served as the starting point of the application.
Listed all available routes.

/api/v1.0/precipitation:

Converted the query results from the precipitation analysis to a dictionary format.
Returned the JSON representation of the dictionary.

/api/v1.0/stations:

Returned a JSON list of stations from the dataset.

/api/v1.0/tobs:

Queried the dates and temperature observations of the most-active station for the previous year of data.
Returned a JSON list of temperature observations for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>:

Calculated the minimum, average, and maximum temperatures for a specified start or start-end range.
For a specified start date, calculated TMIN, TAVG, and TMAX for dates greater than or equal to the start date.
For a specified start and end date, calculated TMIN, TAVG, and TMAX for dates within the specified range.

The provided Flask routes handled error cases such as invalid date formats or data not found for the specified date or date range. Additionally, the session was properly closed after executing the queries to prevent resource leaks.
