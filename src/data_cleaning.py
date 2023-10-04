import pandas as pd
import numpy as np
import inputs


def run(file_path):
    print(f"Running data cleaning on {file_path}")

    # Read in original data
    raw_ugly_data = pd.read_csv(file_path)

    # Rename columns
    # Some of Strava's column headers are buggy looking!
    for col in raw_ugly_data:
        if '<span class="translation_missing" title="translation missing: ' \
           'en-US.lib.export.portability_exporter.activities.horton_values' in col:
            shortened_col = col.replace(
                '<span class="translation_missing" title="translation missing: '
                'en-US.lib.export.portability_exporter.activities.horton_values',
                '').replace('</span>', '')
            new_col_name = shortened_col.split('>')[1]
            raw_ugly_data.rename(columns={col: new_col_name}, inplace=True)
            print(f'Renamed {col[0:30]}... to {new_col_name}')

    # Drop unneeded columns
    for col in raw_ugly_data:
        if raw_ugly_data[col].isna().sum() == len(raw_ugly_data[col]):
            raw_ugly_data.drop(columns=col, inplace=True)
            print(f'Dropped {col}')

    # Working with Activity date as date-time, and making that info split out into columns
    raw_ugly_data['Activity Date'] = pd.to_datetime(raw_ugly_data['Activity Date'])

    raw_ugly_data['Activity Year'] = raw_ugly_data['Activity Date'].dt.year
    raw_ugly_data['Activity Month'] = raw_ugly_data['Activity Date'].dt.month
    raw_ugly_data['Activity Week'] = raw_ugly_data['Activity Date'].dt.isocalendar().week
    raw_ugly_data['Activity Hour'] = raw_ugly_data['Activity Date'].dt.hour

    # Create new df called cleaned_df. Obviously it is not perfectly cleaned but it's a start!
    cleaned_df = raw_ugly_data.copy()

    return cleaned_df
