import pandas as pd
import numpy as np
import inputs
import seaborn as sns
import matplotlib.pyplot as plt


def create_weekly_avg_df(running_df, num_weeks_current_year: int, num_weeks_first_year: int, num_weeks_typical=52,
                         current_year=2023):
    """

    :param running_df: data frame containing only the running activities
    :param num_weeks_current_year: number of weeks in the current year collected so far, since it is not yet complete
    :param num_weeks_first_year: number of weeks in the first year collected
    :param num_weeks_typical: typical number of weeks in a year to consider, 52 weeks by default
    :param current_year: the current year as an integer, 2023 by default
    :return: data frame with 3 columns: Activity Year, Average Weekly Distance Run in Miles, Average Elapsed Time Run per Week
    """

    # Identify the years for which we have data
    years_studied = running_df['Activity Year'].unique()

    # Initialize the data frame
    weekly_avg_df = pd.DataFrame(
        data={'Activity Year': years_studied, 'Weekly Distance Run (Miles)': np.zeros(len(years_studied)),
              'Elapsed Time Run': np.zeros(len(years_studied))})

    # Establish the first year
    first_year = running_df.reset_index()['Activity Year'][0]

    for year in years_studied:
        if year == first_year:
            weekly_avg = running_df[(running_df['Activity Year'] == year)][
                             ['Activity Week', 'Distance in Miles', 'Elapsed Time']].groupby('Activity Week',
                                                                                             dropna=False).sum().sum() / num_weeks_first_year

        elif year < current_year:
            weekly_avg = running_df[(running_df['Activity Year'] == year)][
                             ['Activity Week', 'Distance in Miles', 'Elapsed Time']].groupby('Activity Week',
                                                                                             dropna=False).sum().sum() / num_weeks_typical

        elif year == current_year:
            weekly_avg = running_df[(running_df['Activity Year'] == year)][
                             ['Activity Week', 'Distance in Miles', 'Elapsed Time']].groupby('Activity Week',
                                                                                             dropna=False).sum().sum() / num_weeks_current_year
        else:
            raise ValueError(
                f"Please check your current_year variable. Is {current_year} less than one of these?: {years_studied}")

        weekly_avg_df.loc[weekly_avg_df['Activity Year'] == year, 'Weekly Distance Run (Miles)'] = weekly_avg[
            'Distance in Miles']
        weekly_avg_df.loc[weekly_avg_df['Activity Year'] == year, 'Elapsed Time Run'] = weekly_avg['Elapsed Time']

    return weekly_avg_df


def create_weekly_avg_graph(weekly_avg_df: pd.DataFrame):
    """

    :param weekly_avg_df: data frame with 3 columns: Activity Year, Average Weekly Distance Run in Miles, Average
    Elapsed Time Run per Week
    :return: graph of average weekly miles run vs. year
    """
    # TODO: ZMcB Oct 4 2023 Add ability to filter by years such as:
    #  [(weekly_avg_df['Activity Year'] > 2018) & (weekly_avg_df['Activity Year'] < 2023)]
    weekly_avg_df_graph = weekly_avg_df.reset_index()

    ax = sns.barplot(data=weekly_avg_df_graph, x='Activity Year', y='Weekly Distance Run (Miles)', palette='flare')
    ax.grid(True, alpha=0.4)  # Add gridlines for better readability
    ax.set_axisbelow(True)
    plt.title('Average Weekly Miles Run')

    x = 0
    for value in weekly_avg_df_graph['Weekly Distance Run (Miles)']:
        plt.text(x=x, y=value + 0.15, s=f"{round(value, 1)}", ha='center')
        x = x + 1
    plt.savefig('output_graphs/averaged_weekly_miles_run.png')
    plt.show()


def create_weekly_time_spent_running_graph(running_df: pd.DataFrame):
    """

    :param running_df: data frame containing only the running activities
    :return: graphs of weekly time spent running per week, split per year
    """
    # Define the years you're interested in
    years = np.arange(running_df['Activity Year'].min(), running_df['Activity Year'].max(), 1)

    # Create a list to store DataFrames for each year
    yearly_dfs = []

    # Loop through each year and create DataFrames for weekly time spent running
    for year in years:
        # Filter data for the current year
        year_data = running_df[running_df['Activity Year'] == year]

        # Group the data by week and sum the 'Moving Time' in seconds
        weekly_time_seconds = year_data.groupby(year_data['Activity Date'].dt.strftime('%U'))['Moving Time'].sum()

        # Convert the summed time to hours
        weekly_time_hours = weekly_time_seconds / 3600  # 3600 seconds in an hour

        # Create a DataFrame for the current year
        yearly_df = pd.DataFrame({
            'Week': np.arange(1, 53),  # All weeks of the year
            'Year': year,
            'Weekly Time Spent Running (hours)': 0  # Initialize all weeks with 0 hours
        })

        # Update weeks with actual data
        weekly_time_hours.index = weekly_time_hours.index.astype(int)  # Convert index to int
        yearly_df['Weekly Time Spent Running (hours)'] = weekly_time_hours.reindex(range(1, 53), fill_value=0).values

        yearly_dfs.append(yearly_df)

    # Concatenate the DataFrames for all years
    merged_df = pd.concat(yearly_dfs, ignore_index=True)

    # Create subplots for each year in a nx1 grid
    fig, axes = plt.subplots(len(years), 1, figsize=(10, 10))  # 4x1 grid

    for i, year in enumerate(years):
        row = i

        # Filter data for the current year
        year_data = merged_df[merged_df['Year'] == year]

        # Create a line plot for the current year
        axes[row].plot(year_data['Week'], year_data['Weekly Time Spent Running (hours)'], marker='o', linestyle='-',
                       label=f'Year {year}')
        axes[row].set_title(f'Weekly Time Spent Running - {year}')
        axes[row].set_xlabel('Week')
        axes[row].set_ylabel('Weekly Hours Run')
        axes[row].legend()

        # Show x-axis tick labels for every nth week (e.g., every 4th week)
        n = 4
        tick_indices = range(0, len(year_data['Week']), n)
        axes[row].set_xticks([year_data['Week'].iloc[i] for i in tick_indices])

        axes[row].grid(True)

    # Adjust subplot layout
    plt.tight_layout()

    plt.savefig('output_graphs/weekly_hours_run.png')

    # Show the plot
    plt.show()
