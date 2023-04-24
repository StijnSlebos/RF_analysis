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

filelist = []
pathlist = Path('RF source/Tomato plant  Run-1 Planar').glob('**/*.csv')
pathlist4 = Path('../../../../Measurement Data/Exp4 _uncal tomato planar/P1_2023-04-21 10-52-22 0').glob('**/*.csv')
pathlist3 = Path('../../../../Measurement Data/Exp 3 Uncal 3kz 1001 point planar tomato/P1 2023-04-19 11-45-51 0').glob('**/*.csv')

for path in pathlist4:
    filelist.append(str(path))
datapoints = len(filelist)

# filelist2 = []
# pathlist2 = Path("../../../../Measurement Data/Exp 3 Uncal 3kz 1001 point planar tomato/P1 2023-04-19 11-45-51 0").glob('**/Trace*.csv')
# for path in pathlist2:
#     filelist2.append(str(path))



# with open('RF source/tr0.csv') as file:
#     data = csv.reader(file, delimiter=',')

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

# start_time = datetime.datetime(2023, 4, 12, hour=16, minute=30, second=20) # measurement 1
# start_time = datetime.datetime(2023, 4, 18, hour=21, minute=41, second=53) # measurement 3
start_time = datetime.datetime(2023, 4, 23, hour=10, minute=46, second=00) # measurement 4
measurement_time = datetime.timedelta(seconds=200)

for i in range(1,datapoints):
    csvdata = pd.read_csv(filelist[i])
    # Get data from right position in CSV/dataframe
    #data = csvdata.iloc[13:,3:5]
    data = csvdata
    # Change types from strings to valid/ plotable types
    data[data.columns[0]] = data[data.columns[0]].astype('int64')
    data[data.columns[1]] = data[data.columns[1]].astype(float)
    # Reshape data
    data = data.rename(columns={data.columns[0]: 'frequency', data.columns[1]: 'S21'})

    measurement = data.set_index('frequency')
    measurements = pd.concat([measurements, measurement], axis=1)

measurement_range = data['frequency'].to_numpy()

dt = measurements['S21'].to_numpy()
dt = dt.transpose()



# data2 = pd.read_csv(filelist[0])
# # data2.head()
# # Get data from right position in CSV/dataframe
# b = data2.iloc[13:,3:5]
# #Change types from strings to valid/ plotable types
# b[b.columns[0]] = b[b.columns[0]].astype('int64')
# b[b.columns[1]] = b[b.columns[1]].astype(float)
# # Reshape data
# b = b.rename(columns={b.columns[0]:'frequency',b.columns[1]:'S11'})
# b = b.set_index('frequency')

# measurement.plot(y='S11', figsize=(9,6))

# a = measurement['S11'].to_numpy()
peak_trend = []
peaks = 0

for i in range(0,datapoints-1):
    a = dt[i][:500]
    peaks_ = find_peaks(a)
    threshold = -40
    while len(peaks_[0]) > 1:
        peaks_ = find_peaks(a, height=threshold)
        threshold = threshold+1
    if len(peaks_[0]) != 0:
        peaks = peaks_[0][0]

    peak_trend.append((start_time+measurement_time*i, measurement_range[peaks], a[peaks]))
#  a[peaks],measurement_range[peaks]
peak_trend = np.array(peak_trend)
peak_trend = peak_trend.transpose()

# print(b.head())

idx = 50

# def customForward(*args):
#     ax2 = plt.gca()
#     fig2 = plt.gcf()
#
#     # get line object...
#     line1 = ax2.get_lines()[0]
#     line2 = ax2.get_lines()[1]
#
#     # ...create some new random data...
#     idx = idx + 1
#     # ...and update displayed data
#     line1.set_ydata(dt[idx])
#     line2.set_xdata(peak_trend[1][idx])
#     line2.set_ydata(peak_trend[2][idx])
#     # ax.set_ylim(min(newData), max(newData))
#     # redraw canvas or new data won't be displayed
#     fig2.canvas.draw()


# monkey patch forward button callback
# NavigationToolbar2Tk.forward = customForward

# plot first data

dt_trend = pd.DataFrame(peak_trend)
dt_trend.to_csv('RF source/export_measurement4.csv')

date_format = mdates.DateFormatter('%H:%M')

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
ax2.plot(peak_trend[1][idx], peak_trend[2][idx], 'r+')
ax2.set_ylabel("transmission (dB)")
ax2.set_xlabel("Frequency (GHz)")
ax2.set_ylim(-90, 0)

fig3, ax3 = plt.subplots(3,1, sharex=True)
ax3[0].plot(peak_trend[0], peak_trend[1])
peak_trend_smooth_sg = savitzky_golay(peak_trend[1], 21, 3,deriv=0, rate=1)
ax3[0].plot(peak_trend[0], peak_trend_smooth_sg, color='green')

ax3[1].plot(peak_trend[0], peak_trend[2])
peak_trend_smooth = peak_trend[2]
for i in range(1, len(peak_trend_smooth)):
    if peak_trend_smooth[i] > -20.552: # use threshold value for now
        peak_trend_smooth[i] = peak_trend_smooth[i-1]
ax3[1].plot(peak_trend[0], peak_trend_smooth, color='red')
peak_trend_smooth_sg = savitzky_golay(peak_trend[2], 21, 3,deriv=0, rate=1)
ax3[1].plot(peak_trend[0], peak_trend_smooth_sg, color='green')
# ax.set_ylim()
ax3[1].set_ylabel("peak gain (dB)")


ax3[0].set_ylabel("f_peak (GHz)")
ax3[2].set_xlabel("time")
ax3[0].xaxis.set_major_formatter(date_format)

ax3[0].grid(True, linestyle='-')
ax3[1].grid(True, linestyle='-')
ax3[2].grid(True, linestyle='-')

plt.show()

a=1
