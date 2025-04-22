#%%
import pandas as pd
from functools import reduce
from pathlib import Path

# Enter the file name
filePath = "2025.04.22_Raw_31.03_V.02.xlsx"

# Enter the timecolumn - datacolumn pairs 
timepairs = {"Date_2278":["Height_2278 [mm]","Temp._2278 [°C]","Batt_2278 [V]"],
            "Date_2279":["Height_2279 [mm]","Temp._2279 [°C]","Batt_2279 [V]"],
            "Date_2224":["Height_2224 [mm]","Temp._2224 [°C]","Batt_2224 [V]"],
            "Date_NFM":["NFM_q [l/s]","NFM_t_water [°C]","NFM_t_air [°C]","NFM_U_batt [V]"]}


#%%
# Load data depending on source type
source = filePath
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
#%%
dataframes = []

for time_col, value_cols in timepairs.items():
    
    for value_col in value_cols:
        temp_df = df[[time_col, value_col]].dropna()
        # Use .loc to modify the datetime column
        temp_df.loc[:, 'datetime'] = pd.to_datetime(temp_df[time_col])
        dataframes.append(temp_df[["datetime",value_col]])

#%%
merged = reduce(lambda left, right: pd.merge(left, right, on='datetime', how='outer'), dataframes)

merged.sort_values('datetime').reset_index(drop=True)

#%%
merged.to_excel("merged_sensors.xlsx")
#%%