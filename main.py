"""
auth: Stijn Slebos ; created on 13/04/2023 ; property of: Imec-OnePlanet

analysis file for csv files coming from RF NA, resulting from measurements

Experiment sample: Tomato with RF planar sensor

"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from pathlib import Path
import datetime

filelist = []
pathlist = Path('RF source/Tomato plant  Run-1 Planar').glob('**/*.csv')
for path in pathlist:
    filelist.append(str(path))
datapoints = len(filelist)

# filelist2 = []
# pathlist2 = Path("../../../../Measurement Data/Exp 3 Uncal 3kz 1001 point planar tomato/P1 2023-04-19 11-45-51 0").glob('**/Trace*.csv')
# for path in pathlist2:
#     filelist2.append(str(path))



# with open('RF source/tr0.csv') as file:
#     data = csv.reader(file, delimiter=',')

measurements = pd.DataFrame({})
measurement_time = []
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


for i in range(0,datapoints):
    csvdata = pd.read_csv(filelist[i])
    # Get data from right position in CSV/dataframe
    data = csvdata.iloc[13:,3:5]
    # Change types from strings to valid/ plotable types
    data[data.columns[0]] = data[data.columns[0]].astype('int64')
    data[data.columns[1]] = data[data.columns[1]].astype(float)
    # Reshape data
    data = data.rename(columns={data.columns[0]: 'frequency', data.columns[1]: 'S11'})

    measurement_time.append(csvdata.loc[4,csvdata.columns[1]])
    measurement = data.set_index('frequency')
    measurements = pd.concat([measurements, measurement], axis=1)

measurement_range = data['frequency'].to_numpy()

dt = measurements['S11'].to_numpy()
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

measurement.plot(y='S11', figsize=(9,6))
a = measurement['S11'].to_numpy()

# print(b.head())

# b.plot(y='Trace ID: ', figsize=(9,6))

fig, ax = plt.subplots()
ax.plot(measurement_range, measurements[0])


a=1
