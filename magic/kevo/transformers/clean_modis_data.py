if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    # Create a variable called df and assign data to it
    df = data

    # Renaming the columns
    df.rename(columns={
        'latitude': 'fire_lat',
        'longitude': 'fire_long',
        'frp': 'fire_radiative_power'
    }, inplace=True)

    # Handle any invalid time data
    df['acq_time'] = df['acq_time'].astype(str).str.zfill(4)  # Add leading zeros if necessary

    # Correct any formatting issues
    df['acq_time'] = df['acq_time'].str.replace(r'[^0-9]', '', regex=True)  # Remove non-numeric characters
    df['acq_time'] = df['acq_time'].str.zfill(4)  # Ensure the time is in HHMM format

    # Convert to HH:MM format
    df['acq_time'] = df['acq_time'].str[:2] + ':' + df['acq_time'].str[2:]

    # Step 2: Combine 'acq_date' and 'acq_time' to create a timestamp
    df['modis_timestamp'] = pd.to_datetime(df['acq_date'] + ' ' + df['acq_time'], format='%Y-%m-%d %H:%M')

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
