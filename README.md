# sqlalchemy-challenge
Module 10 SQLAlchemy challenge

## Part One: Analysis and Exploration

Using Python and SQLAlchemy, I connected to our hawaii SQL database containing a station and measurement table. Using the precipitation table, I did the following:

    Found the most recent date in the dataset
    Queried and calculated the previous 12 months of precipitation data from most recent date
    Loaded the query results into a DataFrame with the index as date
    Sorrt the DataFrame by 'date'
    Plotted the results of the precipitation data using matplotlib
    Printed the summary statistics for precipitation data using Pandas

Next, using the stations data, I did the following:

        Queried the total number of stations in the dataset
        Queried the most active station by listing the stations and observation count
        Queried the lowest, highest, and average temperatures for the most active station
        Queried the previous 12 motnhs of temperature observations
        Plotted the previous querry as a histogram with 12 bins

## Part Two: Designing the App

After our analysis, I moved on to design a Flask API based on our previous querries. The Flask App has the following routes:

Welcome:

    Lists all availible routes

Precipitation:

    Converts query results from precipitation analysis and returns it as a JSON

Stations:

    Returns a JSON list of all stations in the dataset

Temperature:

    Querries the dates and temperature observations of the most active station over the past year
    Returns a JSON of those temperature observations

Dates:
    Returns a JSON list of minimum, maximum, and average termerature for a specified start or start-end date range.