import pandas as pd
from functools import reduce
from pathlib import Path

def merge_data(source,timepairs:dict):
    """
    Merge time-aligned sensor data from multiple columns into a single DataFrame.

    Parameters:
    -----------
    source : str or pandas.DataFrame
        Either a file path to a supported file format (.xlsx, .xls, .csv, .json),
        or an already-loaded pandas DataFrame.

    timepairs : dict
        Dictionary mapping time column names to a list of sensor value columns.
        Example:
        {
            "Date_col1": ["val_col1", "val_col2"],
            "Date_col2": ["val_col3", "val_col4"]
        }

    Returns:
    --------
    pandas.DataFrame
        A merged DataFrame with a single 'datetime' column and each sensor value
        as a separate column. Data is outer-joined on timestamps and sorted by time.

    Example:
    --------
    df = merge_data("sensor_data.xlsx", {
            "Date_col1": ["val_col1", "val_col2"],
            "Date_col2": ["val_col3", "val_col4"]
    })
    """
    # Load data depending on source type
    # Load data depending on source type
    if isinstance(source, str):
        ext = Path(source).suffix.lower()
        if ext in ['.xlsx', '.xls']:
            df = pd.read_excel(source)
        elif ext == '.csv':
            df = pd.read_csv(source)
        elif ext == '.json':
            df = pd.read_json(source)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    elif isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        raise ValueError("source must be a file path (str) or a pandas DataFrame.")

    dataframes = []

    for time_col, value_cols in timepairs.items():
        
        for value_col in value_cols:
            temp_df = df[[time_col, value_col]].dropna()
            temp_df.columns = ['datetime', value_col]
            # Use .loc to modify the datetime column
            temp_df.loc[:, 'datetime'] = pd.to_datetime(temp_df['datetime'])
            dataframes.append(temp_df)

    merged = reduce(lambda left, right: pd.merge(left, right, on='datetime', how='outer'), dataframes)

    return merged.sort_values('datetime').reset_index(drop=True)
