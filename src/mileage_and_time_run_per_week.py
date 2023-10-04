import pandas as pd
import numpy as np
import inputs
import seaborn as sns
import matplotlib.pyplot as plt


def create_weekly_avg_df(running_df, num_weeks_current_year: int, num_weeks_typical=52, current_year=2023):
    """

    :param running_df: data frame containing only the running activities
    :param num_weeks_current_year: number of weeks in the current year collected so far, since it is not yet complete
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

    for year in years_studied:
        if year < current_year:
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


def create_weekly_avg_graph(weekly_avg_df):
    weekly_avg_df_graph = weekly_avg_df[
        (weekly_avg_df['Activity Year'] > 2018) & (weekly_avg_df['Activity Year'] < 2023)].reset_index()

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
