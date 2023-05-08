# New start analyisis file for running and analyzing and experiment
import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from SGfunc import savitzky_golay

from scipy.signal import find_peaks
from pathlib import Path
import datetime




# Loading in data from all sources


# Setting the measurement settings


#

def load_rf_measurement(folder_path, type='double'):
    filelist = []
    for path in folder_path:
        filelist.append(str(path))
    files = len(filelist)
    measurements_sensor_1 = pd.DataFrame({})
    measurements_sensor_2 = pd.DataFrame({})

    measurement_range_sensor_1 = []
    measurement_range_sensor_2 = []

    if type == 'single':
        for i in range(0,files):
            csvdata = pd.read_csv(filelist[i])
            data = csvdata
            data[data.columns[0]] = data[data.columns[0]].astype('int64')
            data[data.columns[1]] = data[data.columns[1]].astype(float)
            # Reshape data
            data = data.rename(columns={data.columns[0]: 'frequency', data.columns[1]: 'S21'})
            measurement = data.set_index('frequency')
            measurements_sensor_1 = pd.concat([measurements_sensor_1, measurement], axis=1)
        measurement_range_sensor_1 = data['frequency'].to_numpy()

        dt = measurements_sensor_1['S21'].to_numpy().transpose()


    elif type == 'double':
        for i in range(0,files,2):
            #LOAD PART sensor 1
            csvdata_sensor_1 = pd.read_csv(filelist[i])
            data_sensor_1 = csvdata_sensor_1
            data_sensor_1[data_sensor_1.columns[0]] = data_sensor_1[data_sensor_1.columns[0]].astype('int64')
            data_sensor_1[data_sensor_1.columns[1]] = data_sensor_1[data_sensor_1.columns[1]].astype(float)
            # Reshape data
            data_sensor_1 = data_sensor_1.rename(columns={data_sensor_1.columns[0]: 'frequency', data_sensor_1.columns[1]: 'S21'})
            measurement_sensor1 = data_sensor_1.set_index('frequency')
            measurements_sensor_1 = pd.concat([measurements_sensor_1, measurement_sensor1], axis=1)
            #LOAD PART sensor 2
            csvdata_sensor_2 = pd.read_csv(filelist[i+1])
            data_sensor_2 = csvdata_sensor_2
            data_sensor_2[data_sensor_2.columns[0]] = data_sensor_2[data_sensor_2.columns[0]].astype('int64')
            data_sensor_2[data_sensor_2.columns[1]] = data_sensor_2[data_sensor_2.columns[1]].astype(float)
            # Reshape data
            data_sensor_2 = data_sensor_2.rename(columns={data_sensor_2.columns[0]: 'frequency', data_sensor_2.columns[1]: 'S21'})
            measurement_sensor2 = data_sensor_2.set_index('frequency')
            measurements_sensor_2 = pd.concat([measurements_sensor_2, measurement_sensor2], axis=1)
        measurement_range_sensor_1 = data_sensor_1['frequency'].to_numpy()
        measurement_range_sensor_2 = data_sensor_2['frequency'].to_numpy()
