import pandas as pd
import numpy as np
import inputs
import seaborn as sns
import matplotlib.pyplot as plt


def run(running_df, start_date, end_date, degree, rounded_running_length):
    # Round 'Distance in Miles' to the nearest mile
    running_df['Rounded Distance'] = np.round(running_df['Distance in Miles'])

    # Group the data by 'Activity Year' and 'Rounded Distance' and count the occurrences
    distance_counts = running_df.groupby(['Activity Year', 'Rounded Distance']).size().unstack(fill_value=0)

    # Create a colormap with a gradient of colors
    cmap = plt.get_cmap('viridis', len(distance_counts.columns))

    # Plot the counts for each Rounded Distance per year with the gradient colormap
    ax = distance_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap=cmap)
    plt.xlabel('Activity Year')
    plt.ylabel('Count')
    plt.title('Rounded Distance Counts per Year')
    plt.xticks(rotation=0)  # Rotate x-axis labels for better visibility

    # Customize the legend with a color bar for the gradient
    legend = plt.legend(title='Rounded Distance', loc='upper right')
    legend.set_bbox_to_anchor((1.25, 1))  # Adjust the legend position

    # Add color patches to the legend for each Rounded Distance
    for i, distance in enumerate(distance_counts.columns):
        legend.get_patches()[i].set_facecolor(cmap(i))

    plt.tight_layout()
    plt.show()
    plt.savefig('output_graphs/rounded_distance_counts_per_year.png')

    # Plotting the counts of mileage run each year, emphasizing most consistent mile run length.
    # Create subplots for each year
    fig, axes = plt.subplots(len(distance_counts.index), 1, figsize=(4, 1.3 * len(distance_counts.index)), sharex=True,
                             sharey=True)

    # Identify top distance run
    top_distance_run = int(distance_counts.sum().index[distance_counts.sum() == distance_counts.sum().max()].values)
    print(f"Most of your runs were around {round(top_distance_run,0)} miles long")

    # Iterate through the years and plot the counts for each Rounded Distance
    for i, year in enumerate(distance_counts.index):
        ax = axes[i]
        counts = distance_counts.loc[year]
        # Highlight top distance run with orange:
        color = ['orange' if index == top_distance_run else 'skyblue' for index in counts.index]
        counts.plot(kind='bar', ax=ax, color=color, label=str(year))
        ax.set_xlabel('Rounded Running Distance (miles)')
        # ax.set_ylabel('Counts of Rounded Distance', labelpad=15)  # Adjust label position
        ax.legend(title='Year', )
        ax.grid(True, alpha=0.3)
        if year == distance_counts.index[0]:
            ax.set_title(f'Number of Runs Completed vs\n Distance (Rounded)')

    # Adjust spacing and layout
    plt.tight_layout()

    plt.savefig('output_graphs/numberruns_vs_distancerounded.png')

    # Show the plot
    plt.show()

    # Pace over time with trend line
    if rounded_running_length=="":
        rounded_running_length = str(top_distance_run)
    else:
        print(f"Using runs of distance {rounded_running_length}...")

    # Filter runs with distances equal to specified number of miles (rounded_running_length)
    filtered_running_df = running_df[running_df['Rounded Distance'] == int(rounded_running_length)].copy()

    # Sort the dataframe by 'Miles Run Last Month' for polynomial fitting
    filtered_running_df.sort_values(by='Activity Date', ascending=True, inplace=True)

    # Create the first plot with the left y-axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Create a line plot to visualize pace over time
    ax1.plot(filtered_running_df.loc[(filtered_running_df['Activity Date'] > start_date) & (
            filtered_running_df['Activity Date'] < end_date), 'Activity Date'], filtered_running_df.loc[
                 (filtered_running_df['Activity Date'] > start_date) & (
                         filtered_running_df['Activity Date'] < end_date), 'Pace in Mins per Mile'], marker='o',
             linestyle='-', color='b', label='Pace')

    # Fit a linear regression trend line
    x = np.arange(len(filtered_running_df[(filtered_running_df['Activity Date'] > start_date) & (filtered_running_df['Activity Date'] < end_date)]))
    y = filtered_running_df.loc[(filtered_running_df['Activity Date'] > start_date) & (
            filtered_running_df['Activity Date'] < end_date), 'Pace in Mins per Mile']
    coefficients = np.polyfit(x, y, degree)
    trend_line = np.poly1d(coefficients)

    ax1.plot(filtered_running_df.loc[(filtered_running_df['Activity Date'] > start_date) & (
            filtered_running_df['Activity Date'] < end_date), 'Activity Date'], trend_line(x), linestyle='--', color='r',
             label='Pace Trend Line')

    # Set axis labels and a title
    ax1.set_xlabel('Activity Date')
    ax1.set_ylabel('Pace (min/mile)')

    # Combine the legends from both axes
    lines, labels = ax1.get_legend_handles_labels()

    if len(rounded_running_length) == 0:
        plt.title('Pace Over Time with Trend Line')
    else:
        plt.title(f"{rounded_running_length} Mile Runs: Pace Over Time with Trend Line")

    # Show the plot
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.legend(lines, labels)
    plt.tight_layout()
    plt.savefig('output_graphs/pace_trend_vs_time.png')
    plt.show()

    # Calculate the mean of the actual values
    mean_actual = np.mean(y)

    # Calculate the sum of squared residuals (SSR)
    ssr = np.sum((y - trend_line(x)) ** 2)

    # Calculate the total sum of squares (SST)
    sst = np.sum((y - mean_actual) ** 2)

    # Calculate R-squared
    r2 = 1 - (ssr / sst)

    print(f'Degree {degree} R-squared: {r2:.4f}')
    print(f'Pace vs Time Maximum Pace: {round(trend_line(x).max(), 2)}')
    print(f'Pace vs Time Minimum Pace: {round(trend_line(x).min(), 2)}')


