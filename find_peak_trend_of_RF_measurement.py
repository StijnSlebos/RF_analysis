import tkinter
from tkinter import filedialog
from pathlib import Path
from sort_files_f import numericalSort

import pandas as pd
import numpy as np
from scipy.signal import find_peaks

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
print("select top level folder")
top_folder_path = filedialog.askdirectory()
top_path_lists = Path(top_folder_path).glob('**/P*')
print("selected top layer folder:" + top_folder_path)

folders = []
index_files = []

for path in top_path_lists:
    if ".CSV" not in str(path):
        folders.append(str(path))
    else:
        index_files.append(str(path))
folders = sorted(folders, key=numericalSort)
index_files = sorted(index_files, key=numericalSort)

sets = len(folders)
total_index = pd.DataFrame({})

number_of_sensors = int(input("Number of RF-sensors used?: (type)  "))
#Concatenate all index files and format in proper fashion
print("indexing files for "+ str(number_of_sensors)+" sensors")
for file, folder in zip(index_files,folders):
    dataf = pd.read_csv(file)
    dataf=dataf.iloc[(3+number_of_sensors):,0:2+number_of_sensors]
    dataf=dataf.rename(columns={dataf.columns[0]: 'time', dataf.columns[1]: 'step'})
    for i in range(0,number_of_sensors):
        dataf = dataf.rename(columns={dataf.columns[2+i]: ('filename_sensor_'+str(i))})
    dataf['time'] = dataf['time'].astype('datetime64[ns]')
    dataf['step'] = dataf['step'].astype('int64')
    for i in range(0, number_of_sensors):
        dataf[('filename_sensor_'+str(i))] = dataf[('filename_sensor_'+str(i))].astype('string')
        dataf[('filename_sensor_'+str(i))] = dataf[('filename_sensor_'+str(i))].str.replace('Trace', folder + "\\Trace")
    total_index = pd.concat([total_index, dataf])

start_time = total_index.iloc[0]['time']
print("measurement started at " + str(start_time))
samples = total_index.shape[0]-1
# samples = 100 # turn on for debug
end_time = total_index.iloc[samples]['time']
print("measurement of "+str(samples)+" samples, end time set to " + str(end_time))

#now start with interpreting the actual data per file
measurements = [pd.DataFrame({})]*number_of_sensors
measurement_time = []
measurement_range = []

print("importing data from samples")
for i in range(0,samples):
    # print("\rreading sample " + str(i), end='\r')
    for s in range(0,number_of_sensors):
        data = pd.read_csv(total_index.iloc[i][('filename_sensor_'+str(s))]+'.csv')
        # Get data from right position in CSV/dataframe (in case of imaginary axis data)
        data = data.iloc[:,0:2]
        # Change types from strings to valid/ plotable types
        data[data.columns[0]] = data[data.columns[0]].astype('int64')
        data[data.columns[1]] = data[data.columns[1]].astype(float)
        # Reshape data
        data = data.rename(columns={data.columns[0]: 'frequency', data.columns[1]: 'S21'})

        measurement = data.set_index('frequency')
        measurements[s] = pd.concat([measurements[s], measurement], axis=1)
    measurement_time.append(total_index.iloc[i]['time'])
    # measurement_time.append(total_index.loc[total_index['step'] == i]['time'].values[0])

peak_measurements = []

for s in range(0,number_of_sensors):
    print("finding peak for sensor " + str(s))
    measurement_range.append(measurements[s].index.to_numpy())

    measurement_data = measurements[s]['S21'].to_numpy()
    measurement_data = measurement_data.transpose()

    # Find lower and upper peaks
    lower_peak_trend = []
    upper_peak_trend = []
    peaks_i = 0
    peaks_u = 0

    for i in range(0, samples):
        a = measurement_data[i]  # [:450] #exist in prior range (ignore right side of spectrum)

        # Upper peak finding
        peaks_ = find_peaks(a)
        threshold = -40
        while len(peaks_[0]) > 1:
            peaks_ = find_peaks(a, height=threshold)
            threshold = threshold + 1
        if len(peaks_[0]) != 0:
            peaks_i = peaks_[0][0]
        upper_peak_trend.append((measurement_time[i], measurement_range[s][peaks_i], a[peaks_i]))

        # Lower peak finding
        peaks_ = find_peaks(-a)
        threshold = 10
        while len(peaks_[0]) > 1:
            peaks_ = find_peaks(-a, height=threshold)
            threshold = threshold + 1
        if len(peaks_[0]) != 0:
            peaks_u = peaks_[0][0]
        lower_peak_trend.append((measurement_time[i], measurement_range[s][peaks_u], a[peaks_u]))

    #  a[peaks],measurement_range[peaks]
    lower_peak_trend = np.array(lower_peak_trend)
    lower_peak_trend = lower_peak_trend.transpose()
    upper_peak_trend = np.array(upper_peak_trend)
    upper_peak_trend = upper_peak_trend.transpose()
    peak_measurements.append([lower_peak_trend,upper_peak_trend])

print("exporting files to: " + top_folder_path)
for s in range(0,number_of_sensors):

    data_to_save = {'time': peak_measurements[s][0][0].transpose() , "[lower peak]\nf_peak (GHz)": peak_measurements[s][0][1].transpose(),"[lower peak]\npeak gain (dB)": peak_measurements[s][0][2].transpose(),  "[upper peak]\nf_peak (GHz)": peak_measurements[s][1][1].transpose(), "[upper peak]\npeak gain (dB)":peak_measurements[s][1][2].transpose()}
    dt_trend = pd.DataFrame(data=data_to_save)
    dt_trend = dt_trend.set_index('time')
    dt_trend.to_csv(top_folder_path+'/peaks-sensor' + str(s)+'.csv')
print("done!")



