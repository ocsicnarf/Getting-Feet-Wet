'''datasets.py
Provides functions to load data from csv files into a format that is
intended for easy use with scikit-learn.

Inspired by the sklearn.datasets module:
http://pydoc.net/scikit-learn/0.9/sklearn.datasets.base
'''

from collections import defaultdict
import cPickle as pickle
import re
import sys
import time
from sklearn.datasets.base import Bunch

DATA_DIR = '~/Desktop/data'
EPISODES_FILE = 'physiological-full-sparse.csv'
EPISODES_PICKLE = EPISODES_FILE.replace('csv', 'pkl')
OUTCOMES_FILE = 'outcomes.csv'

NUM_VARS = 13
_cache = {}

def _float(x):
    try:
        return float(x)
    except ValueError:
        return None
    
def _process_episodes_file(f):
    headers = f.readline().split(',')
    episodes = []
    for line in f:
        split = map(float, re.split(',|:', line))
        id, data = split[0], split[1:]
        max_time = data[-3] # assuming measurements are in chronological order
        episode = defaultdict(list)
        for i in range(0, len(data), 3):
            episode[int(data[i + 1]) - 1].append((data[i],  data[i + 2]))
        episodes.append((id,  episode))
    return headers, episodes

def load_episodes():
    ''' sets up the master dataset from which 
    all other (smaller) datasets are derived
    '''
    start = time.time()
    if 'episodes' in _cache: # check cache first
        return _cache['episodes']
        
    headers, episodes, result = None, None, None
    try:     # try to load from pickle (~25 seconds)
        f = open('/'.join((DATA_DIR, EPISODES_PICKLE)))
        result = pickle.load(f)
    except IOError: # fail gracefully so we can try loading from csv
        pass
    else:
        f.close()

    if result is None: # if no pickle, then load from csv (~60 seconds)
        with open('/'.join((DATA_DIR, EPISODES_FILE))) as f:
            headers, episodes = _process_episodes_file(f)
            result = Bunch(headers=headers, data=episodes)
        with open('/'.join((DATA_DIR, EPISODES_PICKLE)), 'w') as f:
            pickle.dump(result, f) 
    
        
    _cache['episodes'] = result
    
    time_elapsed = time.time() - start
    print 'Loaded', len(result.data), 'episodes in', time_elapsed, 'seconds'
    return result

def load_outcomes():
  if 'outcomes' in _cache: # check cache first
      return _cache['outcomes']
  
  with open('/'.join((DATA_DIR, OUTCOMES_FILE))) as f:
      headers = f.readline()
      outcomes = [] 
      for line in f:
          outcomes.append(map(_float, line.split(',')))
  
  result = Bunch(headers=headers, data=outcomes)
  _cache['outcomes'] = result
  return result

