"""
features.py
===========

Add feature functions here.

"""
import numpy as np

def mean(values, times):
    if values.size > 0:
        return np.mean(values)
    else:
        return 0

def std(values, times):
    if values.size > 0:
        return np.std(values)
    else:
        return 0

def var(values, times):
    if values.size > 0:
        return np.var(values)
    else:
        return 0

def max(values, times):
    if values.size > 0:
        return np.max(values)
    else:
        return 0

def min(values, times):
    if values.size > 0:
        return np.min(values)
    else:
        return 0

def range(values, times):
    if values.size > 0:
        return np.max(values) - np.min(values)
    else:
        return 0

def trend(values, times):
    if times.size < 2:
        return 0
    
    delta_value = values[-1] - values[0]
    delta_time = (times[-1] - times[0])
    delta_days = delta_time / (24 * 60 * 60)
    if delta_time == 0:
        return 0
    else:
        return delta_value / delta_days

# TO DO: add more


STATS = (mean, std, max, min)
TRY_THIS = (mean, std, max, min, trend)


        
