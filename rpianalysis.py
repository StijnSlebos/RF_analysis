import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from SGfunc import savitzky_golay

from scipy.signal import find_peaks
from pathlib import Path
import datetime

raspberrypi_data_csv_path = Path('../../4-19_tomato_rf/STN_Experiment_2023-04-18_12_02_49.csv')
raspberrypi_data = pd.read_csv(raspberrypi_data_csv_path)
# data.loc[data['Sap_flow_SF4M (V)'] == 0 ]

#Remove errors in data from unreliable SDI12 sensors
rpi_data_reform = raspberrypi_data.drop(raspberrypi_data.loc[(raspberrypi_data['Sap_flow_SF4M (V)'] == "['']") | (data['Leaf_Temperature_LC (°C)'] == "['']") |( data['Sap_flow_SF4M (V).1'] == "['']") ].index)

rpi_data_reform['Leaf_Temperature_LC (°C)']=rpi_data_reform['Leaf_Temperature_LC (°C)'].astype('float64')
rpi_data_reform['Sap_flow_SF4M (V)']=rpi_data_reform['Sap_flow_SF4M (V)'].astype('float64')
rpi_data_reform['Sap_flow_SF4M (V).1']=rpi_data_reform['Sap_flow_SF4M (V).1'].astype('float64')

rpi_data_reform = rpi_data_reform.drop(rpi_data_reform.loc[(rpi_data_reform['Leaf_Temperature_LC (°C)'] == 0) | (rpi_data_reform['Sap_flow_SF4M (V)'] == 0) | (rpi_data_reform['Sap_flow_SF4M (V).1'] == 0)].index)

rpi_data_reform[['date', 'time']] = rpi_data_reform['Timestamp'].str.split('_', expand=True)
rpi_data_reform['date'] = rpi_data_reform['date'].astype('datetime64[ns]')
rpi_data_reform['time'] = rpi_data_reform['time'].astype('timedelta64[ns]')

rpi_data_out = rpi_data_reform[['date','time','A14_temperature (°C)','A14_relativeHumidity (%RH)','Leaf_Temperature_LC (°C)','Sap_flow_SF4M (V)','Sap_flow_SF4M (V).1','CO2 (ppm)']].to_numpy()
rpi_data_out = rpi_data_out.transpose()


a = 1