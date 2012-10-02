'''datafiles.py
Provides functions to load data from csv files. Once loaded,
datasets.py converts the data into a format that is
intended for easy use with scikit-learn.
'''

from collections import defaultdict
import cPickle as pickle
import re
import sys
import decorators

DATA_DIR = '../../../Desktop/data'
EPISODES_FILE = 'physiological-full-sparse.csv'
EPISODES_PICKLE = EPISODES_FILE.replace('csv', 'pkl')
OUTCOMES_FILE = 'outcomes.csv'

NUM_VARS = 13

def _float_safe(x):
    try:
        return float(x)
    except ValueError:
        return None
    
def _process_episodes_file(f):
    headers = f.readline().split(',')
    episodes = []
    for line in f:
        split = map(_float_safe, re.split(',|:', line))
        id, data = split[0], split[1:]
        max_time = data[-3] # assuming measurements are in chronological order
        episode = defaultdict(list)
        for i in range(0, len(data), 3):
            episode[int(data[i + 1]) - 1].append((data[i],  data[i + 2]))
        episodes.append((id,  episode))
    return headers, episodes

@decorators.Time
@decorators.Cache
def load_episodes():
    ''' Sets up the master dataset from which 
    all other (smaller) datasets are derived
    '''
    headers, episodes = None, None
    try:     # try to load from pickle (~25 seconds)
        f = open('/'.join((DATA_DIR, EPISODES_PICKLE)))
        header, episodes = pickle.load(f)
    except IOError: # fail gracefully so we can try loading from csv
        pass
    else:
        f.close()

    if episodes is None: # if no pickle, then load from csv (~60 seconds)
        with open('/'.join((DATA_DIR, EPISODES_FILE))) as f:
            headers, episodes = _process_episodes_file(f)
        with open('/'.join((DATA_DIR, EPISODES_PICKLE)), 'w') as f:
            pickle.dump((headers, episodes), f) 

    print '{0} episodes loaded.'.format(len(episodes))
    return headers, episodes

@decorators.Time
@decorators.Cache
def load_outcomes():  
  with open('/'.join((DATA_DIR, OUTCOMES_FILE))) as f:
      headers = f.readline()
      outcomes = [] 
      for line in f:
          outcomes.append(map(_float_safe, line.split(',')))
  
  return headers, outcomes

