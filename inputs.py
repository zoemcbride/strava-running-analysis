###
# This should be the only script you need to touch.
# Update this script and run to see your results analyzed & visualized.
###

import os
from src import data_cleaning


def main():
    print("Welcome to My Strava Analytics Project! :)")

    # Specify the file path location for 'activities.csv' file as a string
    # ie, /Users/zoemcbride/repos/health_running_analysis/strava_export_36240949/activities.csv
    file_path = input("Specify the file path location for 'activities.csv' file: ")

    # Run the data cleaning script
    data_cleaning.run(file_path)

    # Have user validate first fie rows are acceptable



if __name__ == "__main__":
    main()

