import pandas as pd
import tkinter
from tkinter import filedialog

tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
rf_peak_trend_path = filedialog.askopenfile()
rf_peak_trend = pd.read_csv(rf_peak_trend_path)
rf_peak_trend_u = rf_peak_trend.loc[:,['time','[upper peak]\nf_peak (GHz)', '[upper peak]\npeak gain (dB)']]
rf_peak_trend_u['time'] = rf_peak_trend_u['time'].astype('datetime64[ns]')
rf_peak_trend_u['[upper peak]\nf_peak (GHz)'] = rf_peak_trend_u['[upper peak]\nf_peak (GHz)'].astype('int64')
rf_peak_trend_u['[upper peak]\npeak gain (dB)'] = rf_peak_trend_u['[upper peak]\npeak gain (dB)'].astype('float')
rf_peak = rf_peak_trend_u.to_numpy()











a=1