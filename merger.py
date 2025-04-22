#%%
import pandas as pd
from utils import merge_data
import os

filePath = "2025.04.04_Raw_31.03_V.01.xlsx"
filePath = "2025.04.22_Raw_31.03_V.02.xlsx"
filePath = os.path.join("source_data",filePath)
# which date colum (key) has which value columns (list)

timepairs = {"Date_2278":["Height_2278 [mm]","Temp._2278 [°C]","Batt_2278 [V]"],
            "Date_2279":["Height_2279 [mm]","Temp._2279 [°C]","Batt_2279 [V]"],
            "Date_2224":["Height_2224 [mm]","Temp._2224 [°C]","Batt_2224 [V]"],
            "Date_NFM":["Q_NFM [m³/s]","Temp._NFM [°C]","Batt.NFM [V]"]}



timepairs = {"Date_2278":["Height_2278 [mm]","Temp._2278 [°C]","Batt_2278 [V]"],
            "Date_2279":["Height_2279 [mm]","Temp._2279 [°C]","Batt_2279 [V]"],
            "Date_2224":["Height_2224 [mm]","Temp._2224 [°C]","Batt_2224 [V]"],
            "Date_NFM":["NFM_q [l/s]","NFM_t_water [°C]","NFM_t_air [°C]","NFM_U_batt [V]"]}


#%%
merged = merge_data(filePath,timepairs)
merged.to_csv("merged_sensors2.csv",index=False,encoding="utf-8-sig")