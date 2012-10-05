"""
datafiles.py
============
This module provides functions to load data from csv and csv-like files into
memory for easy manipulation. It makes no assumptions about downstream 
processing. (e.g. whether the data is intended to be used with scikit-learn).

"""

from collections import defaultdict
import cPickle as pickle
import re
import sys
import utilities
from utilities import safe_float, safe_int

# Constants
DATA_FOLDER = '../../../Desktop/data'
EPISODES_FILE = 'physiological-full-sparse.csv'
OUTCOMES_FILE = 'outcomes.csv'

EPISODES_PICKLE = EPISODES_FILE.replace('csv', 'pkl')

NUM_VARS = 13

# Internal functions
def _parse_episodes_file(f):
    headers = f.readline().strip().split(',')
    episodes = []
    for line in f:
        split = re.split(',|:', line)
        id, data = int(split[0]), map(safe_float, split[1:])
        episode = defaultdict(list)
        for i in range(0, len(data), 3):
            time, var, value = map(float, data[i:i + 3])
            var = int(var) - 1 # convert for 0-indexing
            episode[var].append((time, value))
        episodes.append((id,  episode))
    return headers, episodes

# Public functions
@utilities.timed
@utilities.cached
@utilities.pickled('/'.join((DATA_FOLDER, EPISODES_PICKLE)))
def load_episodes():
    """ Loads all episode data.
    
    Each of the 7890 episodes contains 13 physiological variables that are
    sampled very sparsely in time. 

    Returns a list of (episode_id, episode_data) tuples. 
    - episode_id is a an integer.
    - episode_data is a list of thirteen lists. Each of the thirteen lists
    contains measurements for a physiological variable. The measurements are
    a (time, value) tuple. Time and value are floats.
    
    """
    with open('/'.join((DATA_FOLDER, EPISODES_FILE))) as f:
        headers, episodes = _parse_episodes_file(f)
            
    print '{0} episodes loaded.'.format(len(episodes))
    return headers, episodes


@utilities.timed
@utilities.cached
def load_outcomes():  
    """ Loads the outcomes associated with each episode.
    
    The columns are:
    - episode_id 
    - length of stay (in seconds?)
    - mortality 0 for died, 1 for lived
    - medical length of stay (some missing values)

    """
    with open('/'.join((DATA_FOLDER, OUTCOMES_FILE))) as f:
        headers = f.readline().strip().split(',')
        outcomes = [] 
        for line in f:
            split = line.split(',')
            id, data = safe_int(split[0]), map(safe_int, split[1:])
            outcomes.append((id, data))
  
    return headers, outcomes

if __name__ == '__main__':
    load_outcomes()
