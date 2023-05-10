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

folders = []
index_files = []

double_sensor = False
# pathlist = Path('../../../../Measurement Data/Trolly measurement/1st measurement').glob('**/Trace Capture*.csv')

# pathlist=Path('../../../../Measurement Data/Trolly measurement/2nd measurement').glob('**/P*')

pathstring = '../Experiments/UNIFARM may experiments/Plant set 1/April 28th RF/Exp1- trail & dry run/Exp1 with only planar'
# pathstring = '../Experiments/May 5th-8th office trolley tomato experiments/Trolly measurement/2nd measurement'

pathlist=Path(pathstring).glob('**/P*')

# pathlist=Path('../../../../Measurement Data/Exp unifarm/Exp1- trail & dry run/Exp1 with only planar').glob('**/P*')
# pathlist=Path('../../../../Measurement Data/Dry run/P4/part 2').glob('**/P*')

for path in pathlist:
    if ".CSV" not in str(path):
        folders.append(str(path))
    else:
        index_files.append(str(path))
folders = sorted(folders, key=numericalSort)
index_files = sorted(index_files, key=numericalSort)

sets = len(folders)
datapoints = (sets)
total_index = pd.DataFrame({})

for i in range(0,sets):
    index = pd.read_csv(index_files[i])
    if double_sensor:
        index = index.iloc[5:, 0:4] #switch 4->5 when having two sensors
        index = index.rename(columns={index.columns[0]: 'time', index.columns[1]: 'step', index.columns[2]: 'filename',  index.columns[3]: 'filename2'})
        index['time'] = index['time'].astype('datetime64[ns]')
        index['step'] = index['step'].astype('int64')
        index['filename'] = index['filename'].astype('string')
        index['filename'] = index['filename'].str.replace('Trace', folders[i] + "\\Trace")
        index['filename2'] = index['filename2'].astype('string')
        index['filename2'] = index['filename2'].str.replace('Trace', folders[i] + "\\Trace")
        total_index = pd.concat([total_index, index])
    else:
        index = index.iloc[4:, 0:3]
        index = index.rename(columns={index.columns[0]: 'time', index.columns[1]: 'step', index.columns[2]: 'filename'})
        index['time'] = index['time'].astype('datetime64[ns]')
        index['step'] = index['step'].astype('int64')
        index['filename'] = index['filename'].astype('string')
        index['filename'] = index['filename'].str.replace('Trace', folders[i]+"\\Trace")
        total_index = pd.concat([total_index, index])
    a=0





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
# start_time = datetime.datetime(2023, 4, 29, hour=5, minute=40, second=2) # measurement P3-2


# measurement_time = datetime.timedelta(seconds=202)
# start_time = total_index.loc[total_index['step']==1]['time'].values[0]
start_time = total_index.iloc[0]['time']
samples = total_index['step'].tail(1).values[0]
samples = total_index.shape[0]-1
# end_time = total_index.loc[total_index['step']==samples]['time'].values[0]
end_time = total_index.iloc[samples]['time']


measurements = pd.DataFrame({})
measurement_time = []
measurement_range = []

for i in range(0,samples):
    # csvdata = pd.read_csv(total_index.loc[total_index['step']==i+1]['filename'].values[0]+'.csv')
    csvdata = pd.read_csv(total_index.iloc[i]['filename']+'.csv')


    # Get data from right position in CSV/dataframe

    data = csvdata.iloc[:,0:2]
    # Change types from strings to valid/ plotable types
    data[data.columns[0]] = data[data.columns[0]].astype('int64')
    data[data.columns[1]] = data[data.columns[1]].astype(float)
    # Reshape data
    data = data.rename(columns={data.columns[0]: 'frequency', data.columns[1]: 'S21'})

    measurement = data.set_index('frequency')
    measurements = pd.concat([measurements, measurement], axis=1)
    measurement_time.append(total_index.iloc[i]['time'])

    # measurement_time.append(total_index.loc[total_index['step'] == i]['time'].values[0])
    s=0

measurement_range = data['frequency'].to_numpy()

dt = measurements['S21'].to_numpy()
dt = dt.transpose()



#Find lower and upper peaks
lower_peak_trend = []
upper_peak_trend = []
peaks_i=0
peaks_u=0

for i in range(0,samples):
    a = dt[i] #exist in prior range (ignore right side of spectrum)

    #Upper peak finding
    peaks_ = find_peaks(a)
    threshold = -40
    while len(peaks_[0]) > 1:
        peaks_ = find_peaks(a, height=threshold)
        threshold = threshold+1
    if len(peaks_[0]) != 0:
        peaks_i = peaks_[0][0]
    upper_peak_trend.append((measurement_time[i], measurement_range[peaks_i], a[peaks_i]))

    #Lower peak finding
    peaks_ = find_peaks(-a)
    threshold = 10
    while len(peaks_[0]) > 1:
        peaks_ = find_peaks(-a, height=threshold)
        threshold = threshold + 1
    if len(peaks_[0]) != 0:
        peaks_u = peaks_[0][0]
    lower_peak_trend.append((measurement_time[i], measurement_range[peaks_u], a[peaks_u]))


#  a[peaks],measurement_range[peaks]
lower_peak_trend = np.array(lower_peak_trend)
lower_peak_trend = lower_peak_trend.transpose()
upper_peak_trend = np.array(upper_peak_trend)
upper_peak_trend = upper_peak_trend.transpose()

lower_peak_trend_f_smooth = savitzky_golay(lower_peak_trend[1], 45, 3,deriv=0, rate=1)
# lower_peak_trend_g_smooth = lower_peak_trend[2]
# for i in range(1, len(lower_peak_trend_g_smooth)):
#     if lower_peak_trend_g_smooth[i] > -15.77: # use threshold value for now
#         lower_peak_trend_g_smooth[i] = lower_peak_trend_g_smooth[i-1]
lower_peak_trend_g_smooth = savitzky_golay(lower_peak_trend[2], 45, 3,deriv=0, rate=1)

upper_peak_trend_f_smooth = savitzky_golay(upper_peak_trend[1], 45, 3,deriv=0, rate=1)
upper_peak_trend_g_smooth = savitzky_golay(upper_peak_trend[2], 45, 3,deriv=0, rate=1)

idx = 80

# ----------------------------------------------------------------------
raspberrypi_data_csv_path = Path('../Experiments/UNIFARM may experiments/Ground truth measurement/GrCh_Experiment_2023-04-20_14_31_01.csv')
# raspberrypi_data_csv_path = Path('../../4-12_tomato_RF/pi_data_4_12/STN_Experiment_2023-04-12_13_57_46 (6).csv')
# raspberrypi_data_csv_path = Path('RPi_sensor_source/GrCh_Experiment_2023-04-20_14_31_01 (3).csv')


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
rpi_data_reform['Timestamp'] = rpi_data_reform['Timestamp'].str.split('_', expand=True)[0]+" "+rpi_data_reform['Timestamp'].str.split('_', expand=True)[1]
rpi_data_reform['Timestamp'] = rpi_data_reform['Timestamp'].astype('datetime64[ns]')
rpidf = rpi_data_reform.set_index('Timestamp')

rpi_data_out = rpi_data_reform[['date','time','A14_temperature (°C)','A14_relativeHumidity (%RH)','Leaf_Temperature_LC (°C)','Sap_flow_SF4M (V)','Sap_flow_SF4M (V).1','CO2 (ppm)']].to_numpy()
rpi_data_out = rpi_data_out.transpose()
# ----------------------------------------------------------------------

#Load in stem data
# stem_data_csv_path = Path('../../../../Measurement Data/stem/3rd exp.txt')
# stem_data_csv_path = Path('../Experiments/UNIFARM may experiments/Ground truth measurement/all days stems diameter unifarm.txt')
stem_data_csv_path = Path('../Experiments/May 5th-8th office trolley tomato experiments/Trolly measurement/new 501 trolley.txt')


stem_data = pd.read_csv(stem_data_csv_path)
# data.loc[data['Sap_flow_SF4M (V)'] == 0 ]

#Remove errors in data from unreliable SDI12 sensors
stem_data[['datetime', 'diameter']] = stem_data['DateTime\tDiameter (mm)'].str.split('\t', expand=True)
stem_data['datetime'] = stem_data['datetime'].astype('datetime64[ns]')
stem_data['diameter'] = stem_data['diameter'].astype('float64')
stdf = stem_data.set_index('datetime')
#
stem_data_out = stem_data[['datetime', 'diameter']].to_numpy().transpose()
# ----------------------------------------------------------------------



# monkey patch forward button callback
# NavigationToolbar2Tk.forward = customForward

# plot first data
end_time_str =  str(end_time.year)+"-"+str(end_time.month)+"-"+str(end_time.day)+" "+str(end_time.hour)+":"+str(end_time.minute)+":"+str(end_time.second)
start_time_str = str(start_time.year)+"-"+str(start_time.month)+"-"+str(start_time.day)+" "+str(start_time.hour)+":"+str(start_time.minute)+":"+str(start_time.second)
stdf = stdf[start_time_str:end_time_str]

data_to_save = {'time': lower_peak_trend[0].transpose() , "[lower peak]\nf_peak (GHz)": lower_peak_trend[1].transpose(),"[lower peak]\npeak gain (dB)": lower_peak_trend[2].transpose(),  "[upper peak]\nf_peak (GHz)": upper_peak_trend[1].transpose(), "[upper peak]\npeak gain (dB)":upper_peak_trend[2].transpose()}
dt_trend = pd.DataFrame(data=data_to_save)
dt_trend = dt_trend.set_index('time')

rpidf = rpidf.resample('30S').mean()
rpidf = rpidf[start_time_str:end_time_str]

exportdt = stdf.join(dt_trend, how='outer').join(rpidf, how='outer')
exportdt.to_csv(pathstring + '/trace_trends.csv')

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
# ax3[0].set_ylim(9.6*10**8,9.9*10**8)

ax3[1].plot(lower_peak_trend[0], lower_peak_trend[2])
ax3[1].plot(lower_peak_trend[0], lower_peak_trend_g_smooth, color='navy', label='low-peak g-shift')
# ax3[1].set_ylim(-75,-65)

ax3[2].plot(upper_peak_trend[0], upper_peak_trend[1])
ax3[2].plot(upper_peak_trend[0], upper_peak_trend_f_smooth, color='crimson', label='high-peak f-shift')
# ax3[2].set_yticks(np.arange(1.522, 1.528,step=0.001))
# ax3[2].set_ylim(1.4*10**9,1.5*10**9)

ax3[3].plot(upper_peak_trend[0], upper_peak_trend[2])
ax3[3].plot(upper_peak_trend[0], upper_peak_trend_g_smooth, color='navy', label='high-peak g-shift')
# ax3[3].set_ylim(-22,-19)
# ax3[3].set_yticks(np.arange( -21, -19,step=0.2))

ax3[4].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[2], color='coral', label='Air temperature')
ax3[4].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[4], color='gold', label='Leaf Temperature')
# ax3[4].set_yticks(np.arange( 19, 20.5,step=0.5))
# ax3[4].set_ylim(19,20.5)
#
ax3[5].plot(rpi_data_out[0]+rpi_data_out[1], (rpi_data_out[5]-0.5)/1.5, color='xkcd:chartreuse', label='Sap flow leaf')
# # ax33b = .twinx()
ax3[5].plot(rpi_data_out[0]+rpi_data_out[1], (rpi_data_out[6]-0.5)/1.5, color='olive', label='Sap flow stem')

# ax3[4].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[2])
# ax3[6].plot(rpi_data_out[0]+rpi_data_out[1], rpi_data_out[7], color='green') #CO2
ax3[6].plot(stem_data_out[0], stem_data_out[1], color='green', label='stem diameter')



ax3[0].set_ylabel("[lower peak]\nf_peak (GHz)")
ax3[1].set_ylabel("[lower peak]\npeak gain (dB)")
ax3[2].set_ylabel("[upper peak]\nf_peak (GHz)")
ax3[3].set_ylabel("[upper peak]\npeak gain (dB)")
ax3[4].set_ylabel("temperature (C)")
ax3[5].set_ylabel("sap Flow (relative %)")
# ax33b.set_ylabel("sap Flow (relative %)", color='green')
# ax3[6].set_ylabel("CO2 (ppm)")
ax3[6].set_ylabel("Stem Diameter (mm)")
ax3[5].set_xlabel("time")
ax3[0].xaxis.set_major_formatter(date_format)
# ax3[0].set_xticklabels(ax3[2].get_xticklabels(), rotation=45)
plt.xticks(rotation=80, ha='right')

ax3[0].set_xlim(lower_peak_trend[0][10], lower_peak_trend[0][-1])
ax3[0].set_xticks(np.arange(lower_peak_trend[0][10], lower_peak_trend[0][-1], datetime.timedelta(hours=1)))


for i in range(0, len(ax3)):
    ax3[i].grid(True, linestyle='-')
    ax3[i].legend(loc='upper right', fontsize='small')


plt.show()

a=1
