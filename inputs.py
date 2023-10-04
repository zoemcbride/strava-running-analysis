###
# This should be the only script you need to touch.
# Update this script and run to see your results analyzed & visualized.
###

import os
from src import data_cleaning
from src.mileage_and_time_run_per_week import *
from utils.running_utils import *
import pandas as pd


def main():
    print("Welcome to My Strava Analytics Project! :)")

    # Specify the file path location for 'activities.csv' file as a string
    # ie, /Users/zoemcbride/repos/health_running_analysis/strava_export_36240949/activities.csv
    file_path = input("Specify the file path location for 'activities.csv' file: ")

    # Run the data cleaning script
    cleaned_df = data_cleaning.run(file_path)

    # Create running dataframe and add distance in miles column
    running_df = create_running_df(cleaned_df)
    running_df = distance_m_to_mi(dataframe=running_df, distance_m_col_name='Distance.1', m_to_mi_conversion=1 / 1610)

    print("\n Created a data frame of running data only...\n")

    # Have user validate first five rows are acceptable
    pd.set_option('display.max_columns', None)
    print(running_df[['Activity Date', 'Activity Name', 'Activity Type', 'Activity Year', 'Activity Month',
                      'Activity Week', 'Distance in Miles']].head())

    logic = input("\n Do the first 5 rows look correct? Note that time is in GMT! Respond True/False: ")

    if logic == "False":
        raise ValueError("Double check the data and try again.")

    # Set up weekly average data frame inputs
    current_year = input("The current year is (if left blank, assumes 2023): ")
    if not current_year:
        current_year = 2023
        print("Assuming 2023...")
    else:
        current_year = int(current_year)

    num_weeks_current_year = input(f"The number of weeks of data collected in {current_year} so far: ")
    if not num_weeks_current_year:
        raise ValueError("Must insert some value")
    else:
        num_weeks_current_year = int(num_weeks_current_year)

    num_weeks_typical = input("The number of weeks per year to consider in a typical year is (if left blank, "
                              "assumes 52): ")
    if not num_weeks_typical:
        num_weeks_typical = 52
        print("Assuming 52 weeks...")
    else:
        num_weeks_typical = int(num_weeks_typical)

    weekly_avg_df = create_weekly_avg_df(running_df, num_weeks_current_year=num_weeks_current_year,
                                         num_weeks_typical=num_weeks_typical, current_year=current_year)
    print("\n Your weekly averages are...\n")
    print(weekly_avg_df)

    print("Create weekly average running graph and save")
    create_weekly_avg_graph(weekly_avg_df)


if __name__ == "__main__":
    main()
