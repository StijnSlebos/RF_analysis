import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from SGfunc import savitzky_golay

from scipy.signal import find_peaks
from pathlib import Path
import datetime

stem_data_csv_path = Path('../../../../Measurement Data/stem/4th exp.txt')
stem_data = pd.read_csv(stem_data_csv_path)
# data.loc[data['Sap_flow_SF4M (V)'] == 0 ]

#Remove errors in data from unreliable SDI12 sensors
stem_data[['datetime', 'diameter']] = stem_data['DateTime\tDiameter (mm)'].str.split('\t', expand=True)
stem_data['datetime'] = stem_data['datetime'].astype('datetime64[ns]')
stem_data['diameter'] = stem_data['diameter'].astype('float64')

stem_data_out = stem_data[['datetime', 'diameter']].to_numpy().transpose()

a=1
