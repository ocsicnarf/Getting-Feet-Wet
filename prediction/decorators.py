"""
utilities.py
============
Various decorator classes and misc. utility functions.

"""
import time
import cPickle as pickle

class timed:
    def __init__(self, function):
        self.function = function
        self.__name__ = function.__name__
    
    def __call__(self, *args):
        start = time.time()
        result = self.function(*args)
        elapsed = time.time() - start
        print '{0} took {1}s'.format(self.function.__name__, round(elapsed, 4))
        return result

class cached:
    def __init__(self, function):
        self.function = function
        self.__name__ = function.__name__
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = self.function(*args)
            return self.cache[args]

class pickled:
    def __init__(self, pickle_path):
        self.pickle_path = pickle_path

    def __call__(self, function):
        def wrapper(*args):
            # try unpickling
            try: 
                file = open(self.pickle_path)
                result = pickle.load(file)
            except IOError:
                pass # fail gracefully
            else:
                file.close()
                return result
            
            # otherwise load from file, and try pickling
            result = function(*args)
            try: 
                file = open(pickle_path)
                pickle.dump(result, file)
            except IOError:
                print 'Error writing to pickle'
            else:
                file.close()
            return result
        return wrapper

class safe:
    def __init__(self, function):
        self.function = function
        self.__name__ = function.__name__

    def __call__(self, *args):
        try:
            return function(*args)
        except:
            return None

@safe
def safe_float(x):
    return float(x)
            
    

    
                

        
