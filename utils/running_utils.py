import pandas as pd
import numpy as np
import inputs


def create_running_df(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """
    cleaned_df: dataframe containing at least column called "Activity Type" and some rows that specify "Run"
    :return: the same dataframe, with only the Run-type rows selected
    """

    unique_activities = cleaned_df['Activity Type'].unique()

    if 'Run' in unique_activities:
        print(f"Your activities included: {unique_activities}")
        running_df = cleaned_df[cleaned_df['Activity Type'] == 'Run'].copy()
    else:
        raise ValueError(f"No running activities recorded. Try again. Activities recorded include: "
                         f"{unique_activities}")

    return running_df


def distance_m_to_mi(dataframe: pd.DataFrame, distance_m_col_name='Distance.1', m_to_mi_conversion=1/1610):
    """
    Should be used for running categories but not super helpful for others!

    Be cognizant that the data provided has TWO distance streams of data. The first one is in mixed units
    (based on the sport) and the second one is in meters, consistently, as far as I can tell.

    dataframe: dataframe that you want to add distance in miles column
    distance_m_col_name: string referring to the name of the column with distance in meters
    m_to_mi_conversion: float constant referring to the conversion factor from meters to miles
    returns dataframe with new column, 'Distance in Miles'


    """

    for index, row in dataframe[distance_m_col_name].items():
        if row is np.nan:
            pass
        else:
            row_mi = row * m_to_mi_conversion
            dataframe.loc[index, 'Distance in Miles'] = row_mi

    return dataframe