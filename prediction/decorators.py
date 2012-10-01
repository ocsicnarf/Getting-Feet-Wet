'''Various decorator classes.'''
import time

class Cache:
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

class Time:
    def __init__(self, function):
        self.function = function
        self.__name__ = function.__name__
    
    def __call__(self, *args):
        start = time.time()
        result = self.function(*args)
        elapsed = time.time() - start
        print '{0} took {1:3f}s'.format(self.function.__name__, elapsed)
        return result
