import pandas as pd
import numpy as np
import inputs
import seaborn as sns
import matplotlib.pyplot as plt


def run(running_df):
    moving_time_in_minutes = running_df['Moving Time'] / 60
    running_df['Pace in Mins per Mile'] = moving_time_in_minutes / running_df['Distance in Miles']

    # HR vs. Pace
    # Define the degree values to test
    degrees_to_test = [3]

    # From playing with this, degrees of 2 and 3 worked the best for my data, though 3 looks slightly better than 2.
    # Greater than degrees = 3, the R^2 value plateaus.

    # Create a function to calculate R-squared
    def calculate_r_squared(x, y, degree):
        # Fit a polynomial regression model
        coefficients = np.polyfit(x, y, degree)

        # Calculate the predicted values using the polynomial model
        predicted_values = np.polyval(coefficients, x)

        # Calculate SST (total sum of squares)
        mean_y = np.mean(y)
        sst = np.sum((y - mean_y) ** 2)

        # Calculate SSE (residual sum of squares)
        sse = np.sum((y - predicted_values) ** 2)

        # Calculate R-squared (R^2)
        r_squared = 1 - (sse / sst)

        return r_squared

    # Sort the data by 'Pace in Mins per Mile'
    running_df_sorted = running_df.sort_values(by='Pace in Mins per Mile')

    # Create a figure to display the plots
    plt.figure(figsize=(12, 6))

    # Create the scatter plot
    plt.scatter(running_df_sorted['Pace in Mins per Mile'], running_df_sorted['Average Heart Rate'], label='Average HR',
                marker='o')
    plt.scatter(running_df_sorted['Pace in Mins per Mile'], running_df_sorted['Max Heart Rate'], label='Max HR',
                marker='x')

    # Drop rows with NaN values in 'Pace in Mins per Mile', 'Average Heart Rate', and 'Max Heart Rate' columns
    running_df_cleaned = running_df_sorted.dropna(
        subset=['Pace in Mins per Mile', 'Average Heart Rate', 'Max Heart Rate'])

    # Initialize a dictionary to store R^2 values for each degree
    r_squared_values = {}

    for degree in degrees_to_test:
        # Fit a polynomial regression line for 'Average Heart Rate' in the cleaned dataset
        coefficients_avg = np.polyfit(running_df_cleaned['Pace in Mins per Mile'],
                                      running_df_cleaned['Average Heart Rate'], degree)

        # Fit a polynomial regression line for 'Max Heart Rate' in the cleaned dataset
        coefficients_max = np.polyfit(running_df_cleaned['Pace in Mins per Mile'], running_df_cleaned['Max Heart Rate'],
                                      degree)

        # Calculate R-squared (R^2) for 'Average Heart Rate'
        r_squared_avg = calculate_r_squared(running_df_cleaned['Pace in Mins per Mile'],
                                            running_df_cleaned['Average Heart Rate'], degree)

        # Calculate R-squared (R^2) for 'Max Heart Rate'
        r_squared_max = calculate_r_squared(running_df_cleaned['Pace in Mins per Mile'],
                                            running_df_cleaned['Max Heart Rate'], degree)

        # Store the R^2 values in the dictionary
        r_squared_values[f'Degree {degree} (Average HR)'] = round(r_squared_avg, 2)
        r_squared_values[f'Degree {degree} (Max HR)'] = round(r_squared_max, 2)

        # Plot the polynomial regression lines
        plt.plot(
            running_df_cleaned['Pace in Mins per Mile'],
            np.polyval(coefficients_avg, running_df_cleaned['Pace in Mins per Mile']),
            label=f'Trend Line (Average HR) Degree {degree}, R^2={round(r_squared_avg, 2)}',
        )
        plt.plot(
            running_df_cleaned['Pace in Mins per Mile'],
            np.polyval(coefficients_max, running_df_cleaned['Pace in Mins per Mile']),
            label=f'Trend Line (Max HR) Degree {degree}, R^2={round(r_squared_max, 2)}',
        )

    # Set axis labels and a legend
    plt.xlabel('Pace (min/mile)')
    plt.ylabel('Heart Rate (BPM)')
    plt.legend()

    # Show the plot
    plt.grid(True)  # Add gridlines for better readability
    plt.title('Heart Rate vs. Pace')
    plt.savefig('output_graphs/heartrate_vs_pace.png')
    plt.show()

    # Print the R^2 values for each degree
    for degree, r_squared in r_squared_values.items():
        print(f'HR vs Pace - R-squared (R^2) {degree}: {r_squared}')


    # HR vs. Apparent temperature
    # Convert apparent temperature from Celsius to Fahrenheit
    running_df['Apparent Temperature (Fahrenheit)'] = (running_df['Apparent Temperature'] * 9 / 5) + 32

    # Establish the size of the figure
    plt.figure(figsize=(12, 6))

    # Create the scatter plot
    plt.scatter(running_df['Apparent Temperature (Fahrenheit)'], running_df['Average Heart Rate'], label='Average HR',
                marker='o')
    plt.scatter(running_df['Apparent Temperature (Fahrenheit)'], running_df['Max Heart Rate'], label='Max HR',
                marker='x')

    # Set axis labels and a legend
    plt.xlabel('Apparent Temperature (*F)')
    plt.ylabel('Heart Rate (BPM)')
    plt.legend()

    # Show the plot
    plt.grid(True)  # Add gridlines for better readability
    plt.title('Heart Rate vs. Apparent Temperature')
    plt.savefig('output_graphs/heartrate_vs_apparenttemp.png')
    plt.show()
