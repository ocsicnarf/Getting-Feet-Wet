"""
datasets.py
===========

This module takes data provided by the datafiles module and
prepares datasets intended for use with scikit-learn
algorithms. 

The datasets are returned as Bunch objects, which are essentially
dictionaries with entries exposed as attributes, e.g.
    
>>> my_bunch_object.key
value 

These datasets are modeled after those provided by the scikit-learn 
in its sklearn.datasets module, linked below:
http://pydoc.net/scikit-learn/0.9/sklearn.datasets.base

"""

import numpy as np
from sklearn.datasets.base import Bunch
import datafiles
import utilities
from utilities import unzip

NUM_STATS = 4

def _compute_stats(values):
    """ Compute basic statistics for a 1d array of values """
    # excluded variance (redundant with standard deviation)
    stats = [values.mean(), values.std(), values.max(), values.min()] 
    return stats

@utilities.timed
@utilities.cached
def load_physio_stats():
    description = """ Loads a dataset containing physiological data. 

    It returns a Bunch with the following attributes:
    - data: n_samples by n_features 2D array. There are 7890 samples
    (patient episodes), and 52 features (mean, standard deviation, max
    and min for each of 13 physiological variables)
    - c_target: target variable to be used for classification: mortality.
    0 indicates survival, 1 indicates death.
    - r_target: target variable to be used for regression: length of stay 
    in days.
    - DESCR: a description of this dataset (for now, the docstring of 
    this function)

    """
    headers, episodes = datafiles.load_episodes()
    headers, outcomes = datafiles.load_outcomes() # don't care about headers
    
    # construct the prediction dataset
    num_samples = len(episodes)
    num_features = NUM_STATS * datafiles.NUM_VARS
    data = np.zeros((num_samples, num_features))  

    # for each sample (episode)
    for i, (episode_id, episode_data) in enumerate(episodes):
        # compute its features (stats for each physiological variable)
        for v in range(datafiles.NUM_VARS):
            if episode_data[v]:
                times, values = unzip(episode_data[v])
                times = np.asarray(times)
                values = np.asarray(values)
                data[i, v * NUM_STATS:(v + 1) * NUM_STATS] = \
                    _compute_stats(values)
    
    # obtain the target variables
    episode_ids, episode_outcomes = unzip(outcomes) 

    # mortality, for classification
    c_target = np.asarray(unzip(episode_outcomes)[1])  
    
    # length of stay, for regression
    r_target = np.asarray(unzip(episode_outcomes)[0])
    r_target = np.floor(r_target / (24 * 60 * 60)) # convert from secs to days

    result = Bunch(data=data,
                   r_target=r_target, 
                   c_target=c_target,
                   DESCR=description) 
    return result



