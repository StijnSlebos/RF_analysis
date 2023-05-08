"""
auth: Stijn Slebos ; created on 13/04/2023 ; property of: Imec-OnePlanet

analysis file for csv files coming from RF NA, resulting from measurements

Experiment sample: Tomato with RF planar sensor

"""

import csv
import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from SGfunc import savitzky_golay

from scipy.signal import find_peaks
from pathlib import Path
import datetime

import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

filelist = []
pathlist = Path('RF source/Tomato plant  Run-1 Planar').glob('**/*.csv')
pathlist4 = Path('../../../../Measurement Data/Exp4 _uncal tomato planar/P1_2023-04-21 10-52-22 0').glob('**/*.csv')
pathlist3 = Path('../../../../Measurement Data/Exp 3 Uncal 3kz 1001 point planar tomato/P1 2023-04-19 11-45-51 0').glob('**/*.csv')
pathlist_GrCH2 = Path('RF source/3_5/3_5/P3 full scale/PA/PA2 2023-05-03 12-22-08 0').glob('**/Trace Capture*.csv')

for path in pathlist_GrCH2:
    filelist.append(str(path))
filelist = sorted(filelist, key=numericalSort)
files = len(filelist)
datapoints = (files)/2

measurements = pd.DataFrame({})
measurement_range = []

# measurements2 = pd.DataFrame({})
# for i in range(0, len(filelist2)):
#     csvdata = pd.read_csv(filelist2[i])
#     # Get data from right position in CSV/dataframe
#     data = csvdata.iloc[13:, 3:5]
#     # Change types from strings to valid/ plotable types
#     data[data.columns[0]] = data[data.columns[0]].astype('int64')
#     data[data.columns[1]] = data[data.columns[1]].astype(float)
#     # Reshape data
#     data = data.rename(columns={data.columns[0]: 'frequency', data.columns[1]: 'S11'})
#
#     measurement_time.append(csvdata.loc[4, csvdata.columns[1]])
#     measurement = data.set_index('frequency')
#     measurements = pd.concat([measurements, measurement], axis=1)

# Configure start time and delta of measurement

# start_time = datetime.datetime(2023, 4, 12, hour=16, minute=30, second=20) # measurement 1
# start_time = datetime.datetime(2023, 4, 18, hour=21, minute=41, second=53) # measurement 3
# start_time = datetime.datetime(2023, 4, 20, hour=10, minute=46, second=00) # measurement 4
start_time = datetime.datetime(2023, 4, 29, hour=5, minute=40, second=2) # measurement P3-2


measurement_time = datetime.timedelta(seconds=202)

for i in range(0,files,2):
    csvdata = pd.read_csv(filelist[i+1])
    # Get data from right position in CSV/dataframe
    # data = csvdata.iloc[13:,3:5]
    data = csvdata.iloc[:,0:2]
    # Change types from strings to valid/ plotable types
    data[data.columns[0]] = data[data.columns[0]].astype('int64')
    data[data.columns[1]] = data[data.columns[1]].astype(float)
    # Reshape data
    data = data.rename(columns={data.columns[0]: 'frequency', data.columns[1]: 'S21'})

    measurement = data.set_index('frequency')
    measurements = pd.concat([measurements, measurement], axis=1)
    s=0

measurement_range = data['frequency'].to_numpy()

dt = measurements['S21'].to_numpy()
dt = dt.transpose()



#Find lower and upper peaks
lower_peak_trend = []
upper_peak_trend = []
peaks_i=0
peaks_u=0

for i in range(0,int(datapoints)):
    a = dt[i] #exist in prior range (ignore right side of spectrum)

    #Upper peak finding
    peaks_ = find_peaks(a)
    threshold = -40
    while len(peaks_[0]) > 1:
        peaks_ = find_peaks(a, height=threshold)
        threshold = threshold+1
    if len(peaks_[0]) != 0:
        peaks_i = peaks_[0][0]
    upper_peak_trend.append((start_time+measurement_time*i, measurement_range[peaks_i], a[peaks_i]))

    #Lower peak finding
    peaks_ = find_peaks(-a)
    threshold = 10
    while len(peaks_[0]) > 1:
        peaks_ = find_peaks(-a, height=threshold)
        threshold = threshold + 1
    if len(peaks_[0]) != 0:
        peaks_u = peaks_[0][0]
    lower_peak_trend.append((start_time + measurement_time * i, measurement_range[peaks_u], a[peaks_u]))


#  a[peaks],measurement_range[peaks]
lower_peak_trend = np.array(lower_peak_trend)
lower_peak_trend = lower_peak_trend.transpose()
upper_peak_trend = np.array(upper_peak_trend)
upper_peak_trend = upper_peak_trend.transpose()

lower_peak_trend_f_smooth = savitzky_golay(lower_peak_trend[1], 21, 3,deriv=0, rate=1)
# lower_peak_trend_g_smooth = lower_peak_trend[2]
# for i in range(1, len(lower_peak_trend_g_smooth)):
#     if lower_peak_trend_g_smooth[i] > -15.77: # use threshold value for now
#         lower_peak_trend_g_smooth[i] = lower_peak_trend_g_smooth[i-1]
lower_peak_trend_g_smooth = savitzky_golay(lower_peak_trend[2], 21, 3,deriv=0, rate=1)

upper_peak_trend_f_smooth = savitzky_golay(upper_peak_trend[1], 21, 3,deriv=0, rate=1)
upper_peak_trend_g_smooth = savitzky_golay(upper_peak_trend[2], 21, 3,deriv=0, rate=1)

idx = 80

# ----------------------------------------------------------------------
# raspberrypi_data_csv_path = Path('../../4-19_tomato_rf/STN_Experiment_2023-04-18_12_02_49.csv') # experiment 3
# raspberrypi_data_csv_path = Path('../../4-12_tomato_RF/pi_data_4_12/STN_Experiment_2023-04-12_13_57_46 (6).csv')
raspberrypi_data_csv_path = Path('RPi_sensor_source/GrCh_Experiment_2023-04-20_14_31_01 (3).csv')


raspberrypi_data = pd.read_csv(raspberrypi_data_csv_path)
# data.loc[data['Sap_flow_SF4M (V)'] == 0 ]

# Remove errors in data from unreliable SDI12 sensors
rpi_data_reform = raspberrypi_data.drop(raspberrypi_data.loc[(raspberrypi_data['Sap_flow_SF4M (V)'] == "['']") | (raspberrypi_data['Leaf_Temperature_LC (°C)'] == "['']") |( raspberrypi_data['Sap_flow_SF4M (V).1'] == "['']") ].index)

rpi_data_reform['Leaf_Temperature_LC (°C)']=rpi_data_reform['Leaf_Temperature_LC (°C)'].astype('float64')
rpi_data_reform['Sap_flow_SF4M (V)']=rpi_data_reform['Sap_flow_SF4M (V)'].astype('float64')
rpi_data_reform['Sap_flow_SF4M (V).1']=rpi_data_reform['Sap_flow_SF4M (V).1'].astype('float64')

rpi_data_reform = rpi_data_reform.drop(rpi_data_reform.loc[(rpi_data_reform['Leaf_Temperature_LC (°C)'] == 0) | (rpi_data_reform['Sap_flow_SF4M (V)'] == 0) | (rpi_data_reform['Sap_flow_SF4M (V).1'] == 0)].index)

rpi_data_reform[['date', 'time']] = rpi_data_reform['Timestamp'].str.split('_', expand=True)
rpi_data_reform['date'] = rpi_data_reform['date'].astype('datetime64[ns]')
rpi_data_reform['time'] = rpi_data_reform['time'].astype('timedelta64[ns]')

rpi_data_out = rpi_data_reform[['date','time','A14_temperature (°C)','A14_relativeHumidity (%RH)','Leaf_Temperature_LC (°C)','Sap_flow_SF4M (V)','Sap_flow_SF4M (V).1','CO2 (ppm)']].to_numpy()
rpi_data_out = rpi_data_out.transpose()
# ----------------------------------------------------------------------

#Load in stem data
# stem_data_csv_path = Path('../../../../Measurement Data/stem/3rd exp.txt')
# stem_data_csv_path = Path('../../../../Measurement Data/stem/4th exp.txt')

# stem_data = pd.read_csv(stem_data_csv_path)
# data.loc[data['Sap_flow_SF4M (V)'] == 0 ]

#Remove errors in data from unreliable SDI12 sensors
# stem_data[['datetime', 'diameter']] = stem_data['DateTime\tDiameter (mm)'].str.split('\t', expand=True)
# stem_data['datetime'] = stem_data['datetime'].astype('datetime64[ns]')
# stem_data['diameter'] = stem_data['diameter'].astype('float64')
#
# stem_data_out = stem_data[['datetime', 'diameter']].to_numpy().transpose()
# ----------------------------------------------------------------------



# monkey patch forward button callback
# NavigationToolbar2Tk.forward = customForward

# plot first data

dt_trend = pd.DataFrame(lower_peak_trend)
dt_trend.to_csv('RF source/export_measurement4.csv')

date_format = mdates.DateFormatter('%d/%d %H:%M')

# plot trend in peak value
# fig, ax = plt.subplots()
# ax.plot(peak_trend[0], peak_trend[2])
#
# peak_trend_smooth = peak_trend[2]
# for i in range(1, len(peak_trend_smooth)):
#     if peak_trend_smooth[i] > -15.77:
#         peak_trend_smooth[i] = peak_trend_smooth[i-1]
# ax.plot(peak_trend[0], peak_trend_smooth, color='red')
#
# peak_trend_smooth_sg = savitzky_golay(peak_trend[2], 17, 4,deriv=0, rate=1)
# ax.plot(peak_trend[0], peak_trend_smooth_sg, color='green')
# # ax.set_ylim()
# ax.set_ylabel("peak gain (dB)")
# ax.set_xlabel("time")
# ax.xaxis.set_major_formatter(date_format)
# plt.show()


fig2, ax2 = plt.subplots()
ax2.plot(measurement_range, dt[idx])
ax2.plot(lower_peak_trend[1][idx], lower_peak_trend[2][idx], 'r+')
ax2.plot(upper_peak_trend[1][idx], upper_peak_trend[2][idx], 'r+')
ax2.set_ylabel("transmission (dB)")
ax2.set_xlabel("Frequency (GHz)")
ax2.set_ylim(-90, 0)

fig3, ax3 = plt.subplots(7,1, sharex=True)


ax3[0].plot(lower_peak_trend[0], lower_peak_trend[1])
ax3[0].plot(lower_peak_trend[0], lower_peak_trend_f_smooth, color='crimson', label='low-peak f-shift')

ax3[1].plot(lower_peak_trend[0], lower_peak_trend[2])
ax3[1].plot(lower_peak_trend[0], lower_peak_trend_g_smooth, color='navy', label='low-peak g-shift')

ax3[2].plot(upper_peak_trend[0], upper_peak_trend[1])
ax3[2].plot(upper_peak_trend[0], upper_peak_trend_f_smooth, color='crimson', label='high-peak f-shift')
# ax3[2].set_yticks(np.arange(1.522, 1.528,step=0.001))

ax3[3].plot(upper_peak_trend[0], upper_peak_trend[2])
ax3[3].plot(upper_peak_trend[0], upper_peak_trend_g_smooth, color='navy', label='high-peak g-shift')
# ax3[3].set_yticks(np.arange( -21, -19,step=0.2))

ax3[4].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[2], color='coral', label='Air temperature')
ax3[4].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[4], color='gold', label='Leaf Temperature')
ax3[4].set_yticks(np.arange( 19, 20.5,step=0.5))
ax3[4].set_ylim(19,20.5)

ax3[5].plot(rpi_data_out[0]+rpi_data_out[1], (rpi_data_out[5]-0.5)/1.5, color='xkcd:chartreuse', label='Sap flow leaf')
# ax33b = .twinx()
ax3[5].plot(rpi_data_out[0]+rpi_data_out[1], (rpi_data_out[6]-0.5)/1.5, color='olive', label='Sap flow stem')

# ax3[4].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[2])
# ax3[6].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[7], color='green') #CO2
# ax3[6].plot(stem_data_out[0], stem_data_out[1], color='green', label='stem diameter')



ax3[0].set_ylabel("[lower peak]\nf_peak (GHz)")
ax3[1].set_ylabel("[lower peak]\npeak gain (dB)")
ax3[2].set_ylabel("[upper peak]\nf_peak (GHz)")
ax3[3].set_ylabel("[upper peak]\npeak gain (dB)")
ax3[4].set_ylabel("temperature (C)")
ax3[5].set_ylabel("sap Flow (relative %)")
# ax33b.set_ylabel("sap Flow (relative %)", color='green')
# ax3[6].set_ylabel("CO2 (ppm)")
ax3[6].set_ylabel("Stem Diameter (mm)")
ax3[6].set_xlabel("time")
ax3[0].xaxis.set_major_formatter(date_format)
# ax3[0].set_xticklabels(ax3[2].get_xticklabels(), rotation=45)
plt.xticks(rotation=80, ha='right')

ax3[0].set_xlim(lower_peak_trend[0][0], lower_peak_trend[0][-1])
ax3[0].set_xticks(np.arange(lower_peak_trend[0][0], lower_peak_trend[0][-1], datetime.timedelta(hours=1)))


for i in range(0, len(ax3)):
    ax3[i].grid(True, linestyle='-')
    ax3[i].legend(loc='upper right', fontsize='small')


plt.show()

a=1
