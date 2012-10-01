import datafiles
import time
import numpy as np
from sklearn.datasets.base import Bunch

_cache = {}

def load_physio_stats():
    if _cache.get('physio_stats') is not None:
        return _cache.get('physio_stats')

    # TO DO: check for csv file
    # if file exists, load it from file

    # otherwise, derive it from the master dataset
    episodes = datafiles.load_episodes().data
    outcomes = datafiles.load_outcomes().data
    
    start = time.time();
    # construct the prediction dataset
    num_samples = len(episodes)
    num_features = 5 * datafiles.NUM_VARS
    data = np.zeros((num_samples, num_features))  
    for i, (e_id, e_data) in enumerate(episodes):
        for v in range(datafiles.NUM_VARS):
            if len(e_data[v]) > 0:
                (times, values) = zip(*e_data[v]) # unzips
                times = np.asarray(times)
                values = np.asarray(values)
#                values = values[time < 24 * 60
                data[i, 5*v : 5*v + 5] = \
                    [values.mean(), values.std(), values.max(), values.min(), values.var()]
    
    # Take the "DIED" column to be our target variable
    target = np.asarray(zip(*outcomes)[2]) 

    print 'Loaded prediction dataset in', time.time() - start, 'seconds'
    result = Bunch(data=data, target=target, DESCR="description to be filled in") 
    _cache['physio_stats'] = result
    return result

if __name__ == '__main__':
    load_physio_stats()
