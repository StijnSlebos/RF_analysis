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

with open('RF source/tr0.csv') as file:
    data = csv.reader(file, delimiter=',')

data2 = pd.read_csv('RF source/tr0.csv')
# data2.head()
# Get data from right position in CSV/dataframe
b = data2.iloc[13:,3:5]
#Change types from strings to valid/ plotable types
b[b.columns[0]] = b[b.columns[0]].astype('int64')
b[b.columns[1]] = b[b.columns[1]].astype(float)
# Reshape data
b = b.rename(columns={b.columns[0]:'frequency',b.columns[1]:'S11'})
b = b.set_index('frequency')

b.plot(y='S11', figsize=(9,6))
a = b['S11'].to_numpy()

print(b.head())

# b.plot(y='Trace ID: ', figsize=(9,6))

a=1
