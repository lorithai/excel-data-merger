#%%
import pandas as pd
import os

fileNames = os.listdir("source_data")
filePaths = [os.path.join("source_data",fileName) for fileName in fileNames]
filePaths.sort(key=os.path.getmtime)
filePath = filePaths[0]

timepairs = {"Date_2278":["Height_2278 [mm]","Temp._2278 [°C]","Batt_2278 [V]"],
            "Date_2279":["Height_2279 [mm]","Temp._2279 [°C]","Batt_2279 [V]"],
            "Date_2224":["Height_2224 [mm]","Temp._2224 [°C]","Batt_2224 [V]"],
            "Date_NFM":["Q_NFM [m³/s]","Temp._NFM [°C]","Batt.NFM [V]"]}

#%%
from utils import merge_data

merged = merge_data(filePath,timepairs)
merged.to_csv("merged_sensors.csv",index=False,encoding="utf-8-sig")