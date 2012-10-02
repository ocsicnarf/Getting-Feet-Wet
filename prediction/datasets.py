'''
Returns datasets intended for use with scikit-learn
algorithms. Inspired by the sklearn.datasets module:
http://pydoc.net/scikit-learn/0.9/sklearn.datasets.base
'''

import numpy as np
from sklearn.datasets.base import Bunch
import datafiles
import decorators

NUM_STATS = 4

def compute_stats(values):
    # excluded variance (redundant with standard deviation)
    stats = [values.mean(), values.std(), values.max(), values.min()] 
    return stats

@decorators.Time
@decorators.Cache
def load_physio_stats():
    # if not in cache, derive it from the master dataset
    headers, episodes = datafiles.load_episodes()
    headers, outcomes = datafiles.load_outcomes()
    
    # construct the prediction dataset
    num_samples = len(episodes)
    num_features = NUM_STATS * datafiles.NUM_VARS
    data = np.zeros((num_samples, num_features))  
    for i, (episode_id, episode_data) in enumerate(episodes):
        for v in range(datafiles.NUM_VARS):
            if len(episode_data[v]) > 0:
                times, values = zip(*episode_data[v]) # unzips
                times = np.asarray(times)
                values = np.asarray(values)
                # values = values[time < 24 * 60] 
                data[i, v * NUM_STATS : (v + 1) * NUM_STATS] = \
                    compute_stats(values)
    
    r_target = np.asarray(zip(*outcomes)[1])  # length of stay 
    r_target = np.floor(r_target / (24 * 60 * 60)) # converted from seconds? to days
    c_target = np.asarray(zip(*outcomes)[2])  # mortality. 0/1 = lived/died

    result = Bunch(data=data, DESCR="description to be filled in",
                   r_target=r_target, c_target=c_target) 
    return result



