#sensor data  ingestion pipeline
if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import numpy as np

@custom
def load_data(*args, **kwargs):
    start_time = pd.to_datetime('2025-04-08 00:00:00')
    end_time = pd.to_datetime('2025-04-09 00:00:00')
    timestamps = pd.date_range(start=start_time, end=end_time, freq='T')
    np.random.seed(42)
    sensor_values = np.random.randint(0, 1024, size=len(timestamps))
    
    df = pd.DataFrame({
        'sensor_timestamp': timestamps,
        'sensor_value': sensor_values
    })

    return df


@test
def test_output(df, *args) -> None:
    assert df is not None, 'The output is undefined'
    assert not df.empty, 'The DataFrame is empty'
