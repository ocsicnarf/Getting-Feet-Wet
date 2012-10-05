"""
utilities.py
============
Various decorator classes and misc. utility functions.

"""
import time
import cPickle as pickle

class timed:
    """ Adds timing code to a function. """
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
    """ Caches the result of the function in memory. """
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
    """ Pickles the result of a function. Takes one argument, a file path 
    for the  pickle.
    
    """
    def __init__(self, pickle_path):
        self.pickle_path = pickle_path

    def __call__(self, function):
        class wrapper:
            def __init__(self, function):
                self.function = function
                self.__name__ = function.__name__
            
            def __call__(*args):
                # try unpickling
                try: 
                    file = open(self.pickle_path)
                    result = pickle.load(file)
                except (IOError, EOFError):
                    pass # fail gracefully
                else:
                    file.close()
                    return result
            
                # otherwise load from file, and try pickling
                result = function(*args)
                try: 
                    print self.pickle_path
                    file = open(self.pickle_path, 'w')
                    pickle.dump(result, file)
                except IOError as e:
                    print 'Error writing to pickle.'
                else:
                    file.close()
                return result
        return wrapper(function)

class safe:
    """ Modifies a function to return None instead of throwing an exception """
    def __init__(self, function):
        self.function = function
        self.__name__ = function.__name__

    def __call__(self, *args):
        try:
            return self.function(*args)
        except:
            return None

@safe
def safe_float(s):
    return float(s)
    
@safe
def safe_int(s):
    return int(s)
    
def unzip(zipped):
    return zip(*zipped)

        
