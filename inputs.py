###
# This should be the only script you need to touch.
# Run the script and respond to the prompts to see your results analyzed & visualized.
###

import os
from src import data_cleaning
from src.mileage_and_time_run_per_week import *
from src import heart_rate_influences
from src import pace_over_time
from utils.running_utils import *
import pandas as pd
from datetime import datetime


def get_input_with_default(prompt, default_value, data_type=str):
    user_input = input(prompt)
    return data_type(user_input) if user_input else data_type(default_value)


def get_filepath_input():
    return input("Specify the file path location for 'activities.csv' file: ")


def get_yearly_data_inputs(running_df):
    current_year = get_input_with_default("[Optional] The current year is: ",
                                          running_df.reset_index()['Activity Year'][len(running_df) - 1], int)
    num_weeks_current_year = get_input_with_default(f"[Optional] The number of weeks of data collected in "
                                                    f"{current_year} so far: ",
                                                    running_df.reset_index()['Activity Week'][len(running_df) - 1], int)
    num_weeks_typical = get_input_with_default("[Optional] The number of weeks per year to consider in a typical year "
                                               "is: ", 52, int)
    first_year = running_df.reset_index()['Activity Year'][0]
    num_weeks_first_year = get_input_with_default(f"[Optional] The number of weeks of data collected in {first_year}: ",
                                                  num_weeks_typical - running_df[running_df['Activity Year'] == 2018][
                                                      'Activity Week'].sort_values().reset_index(drop=True)[0], int)

    return current_year, num_weeks_current_year, num_weeks_typical, num_weeks_first_year


def get_pace_over_time_inputs(running_df, first_year):
    start_date = get_input_with_default("[Optional] Specify the start date in format such as 01-01-2019...",
                                        f'01-01-{str(first_year)}')
    end_date = get_input_with_default("[Optional] Specify the end date in format such as 05-01-2023...",
                                      running_df['Activity Date'].sort_values(ascending=False).reset_index(drop=True)[
                                          0].strftime("%m-%d-%Y"))
    degree = get_input_with_default("[Optional] Specify the degree of fit for the pace over time with trend graph...",
                                    3, int)
    rounded_running_length = get_input_with_default(
        "[Optional] Specify the rounded running length, in miles, to assess pace over time...", "")

    return start_date, end_date, degree, rounded_running_length


def main():
    print("Welcome to My Strava Analytics Project! :)")

    # Specify the file path location for 'activities.csv' file as a string
    # ie, /Users/zoemcbride/repos/health_running_analysis/strava_export_36240949/activities.csv
    file_path = get_filepath_input()

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

    print("The following can be inputted, or left blank if you want to assume default: \n")

    # Set up weekly average data frame inputs
    current_year, num_weeks_current_year, num_weeks_typical, num_weeks_first_year = get_yearly_data_inputs(running_df)

    weekly_avg_df = create_weekly_avg_df(running_df, num_weeks_current_year=num_weeks_current_year,
                                         num_weeks_typical=num_weeks_typical, current_year=current_year,
                                         num_weeks_first_year=num_weeks_first_year)
    print("\n Your weekly averages are...\n")
    print(weekly_avg_df)

    print("Creating weekly average running graph and saving in output_graphs/...")
    create_weekly_avg_graph(weekly_avg_df)

    print("Creating weekly average time run graph and saving in output_graphs/...")
    create_weekly_time_spent_running_graph(running_df)

    print("Creating heart rate vs pace and heart rate vs apparent temperature graphs. Saving in output_graphs/...")
    heart_rate_influences.run(running_df)

    # Identify the first year of the data set
    first_year = running_df.reset_index()['Activity Year'][0]

    print("\nThe following apply to the pace over time graphs. These can be inputted, or left blank if you want to"
          " assume default: \n")

    # Specify inputs to pace over time graphs
    start_date, end_date, degree, rounded_running_length = get_pace_over_time_inputs(running_df, first_year)

    print("Creating distance counts per year and number of runs vs distance counts graphs. Saving in output_graphs/...")
    pace_over_time.run(running_df=running_df, start_date=start_date, end_date=end_date, degree=degree,
                       rounded_running_length=rounded_running_length)


if __name__ == "__main__":
    main()
