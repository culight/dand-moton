# import all necessary packages and functions.
import csv
import os
from datetime import datetime,timedelta

import matplotlib as matplotlib
import numpy as np
import pandas as pd
from babs_datacheck import question_3
from babs_visualizations import usage_stats, usage_plot
from IPython.display import display

#%matplotlib inline

# file locations
file_in = '201402_trip_data.csv'
file_out = '201309_trip_data.csv'

def setup():
    with open(file_out, 'w') as f_out, open(file_in, 'r') as f_in:
        # set up csv reader and writer objects
        in_reader = csv.reader(f_in)
        out_writer = csv.writer(f_out)

        # write rows from in-file to out-file until specified date reached
        while True:
            datarow = next(in_reader)
            # trip start dates in 3rd column, m/d/yyyy HH:MM formats
            if datarow[2][:9] == '10/1/2013':
                break
            out_writer.writerow(datarow)

def display_graphs():

    sample_data = pd.read_csv('201309_trip_data.csv')

    display(sample_data.head())

    # Display the first few rows of the station data file.
    station_info = pd.read_csv('201402_station_data.csv')
    display(station_info.head())

    # Process the data by running the function we wrote above.
    station_data = ['201402_station_data.csv']
    trip_in = ['201309_trip_data.csv']
    trip_out = '201309_trip_summary.csv'
    summarise_data(trip_in, station_data, trip_out)

    # Load in the data file and print out the first few rows
    sample_data = pd.read_csv(trip_out)
    display(sample_data.head())

    # Verify the dataframe by counting data points matching each of the time features.
    question_3(sample_data)

# This function will be called by another function later on to create the mapping.
def create_station_mapping(station_data):
    """
    Create a mapping from station IDs to cities, returning the
    result as a dictionary.
    """
    station_map = {}
    for data_file in station_data:
        with open(data_file, 'r') as f_in:
            # set up csv reader object - note that we are using DictReader, which
            # takes the first row of the file as a header row for each row's
            # dictionary keys
            weather_reader = csv.DictReader(f_in)

            for row in weather_reader:
                station_map[row['station_id']] = row['landmark']
    return station_map

def summarise_data(trip_in, station_data, trip_out):
    """
    This function takes trip and station information and outputs a new
    data file with a condensed summary of major trip information. The
    trip_in and station_data arguments will be lists of data files for
    the trip and station information, respectively, while trip_out
    specifies the location to which the summarized data will be written.
    """
    # generate dictionary of station - city mapping
    station_map = create_station_mapping(station_data)

    with open(trip_out, 'w') as f_out:
        # set up csv writer object
        out_colnames = ['duration', 'start_date', 'start_year',
                        'start_month', 'start_hour', 'weekday',
                        'start_city', 'end_city', 'subscription_type']
        trip_writer = csv.DictWriter(f_out, fieldnames=out_colnames)
        trip_writer.writeheader()
        
        print("summarizing data...")

        for data_file in trip_in:
            with open(data_file, 'r') as f_in:
                # set up csv reader object
                trip_reader = csv.DictReader(f_in)

                # collect data from and process each row
                for row in trip_reader:
                    new_point = {}

                    # convert duration units from seconds to minutes
                    ### Question 3a: Add a mathematical operation below   ###
                    ### to convert durations from seconds to minutes.     ###
                    d = float(row['Duration']) / 60.0
                    new_point['duration'] = d

                    # reformat datestrings into multiple columns
                    ### Question 3b: Fill in the blanks below to generate ###
                    ### the expected time values.                         ###
                    trip_date = datetime.strptime(row['Start Date'], '%m/%d/%Y %H:%M')
                    new_point['start_date'] = trip_date.strftime('%Y-%m-%d')
                    new_point['start_year'] = trip_date.year
                    new_point['start_month'] = trip_date.month
                    new_point['start_hour'] = trip_date.hour
                    new_point['weekday'] = trip_date.weekday()

                    # remap start and end terminal with start and end city
                    new_point['start_city'] = station_map[row['Start Terminal']]
                    new_point['end_city'] = station_map[row['End Terminal']]
                    # two different column names for subscribers depending on file
                    if 'Subscription Type' in row:
                        new_point['subscription_type'] = row['Subscription Type']
                    else:
                        new_point['subscription_type'] = row['Subscriber Type']

                    # write the processed information to the output file.
                    trip_writer.writerow(new_point)
                    
def display_usage_stats():
    trip_data = pd.read_csv('201309_trip_summary.csv')
    usage_stats(trip_data)
    usage_plot(trip_data, 'subscription_type')
    usage_plot(trip_data, 'duration', ['duration < 60'], boundary = 0, bin_width = 5)
    
def perform_new_analysis():
    station_data = ['201402_station_data.csv',
                '201408_station_data.csv',
                '201508_station_data.csv' ]
    trip_in = ['201402_trip_data.csv',
               '201408_trip_data.csv',
               '201508_trip_data.csv' ]
    trip_out = 'babs_y1_y2_summary.csv'

    # This function will take in the station data and trip data and
    # write out a new data file to the name listed above in trip_out.
    summarise_data(trip_in, station_data, trip_out)
    
def display_new_graphs():
    trip_data = pd.read_csv('babs_y1_y2_summary.csv')
    display(trip_data.head())
    
def display_new_usage_stats():
    trip_data = pd.read_csv('babs_y1_y2_summary.csv')
    usage_stats(trip_data)
    usage_plot(trip_data, 'start_month', ['start_month < 12'], boundary = 1, bin_width = 1)
    usage_plot(trip_data, 'start_hour', ['start_hour < 23'], boundary = 0, bin_width = 1)

if(os.path.isfile(file_out)):
    #display_graphs()
    #display_usage_stats()
    #perform_new_analysis()
    #display_new_graphs()
    display_new_usage_stats()
else:
    setup()

