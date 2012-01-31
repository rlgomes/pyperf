"""
pyperf is a simple performance measuring library for python which uses python 
decorators to mark the FUNCTIONS you'd want to get performance data. After
marking your FUNCTIONS witht the @pyperf.measure decorator you can then turn 
the library on and off by simply setting the global variable pyperf.PYPERF to 
True. 
"""
import time
import sys
import atexit
import signal

import tableprinter

global FUNCTIONS
FUNCTIONS = {}

global PYPERF
PYPERF = False

global PYPERF_TRACKARGUMENTS
PYPERF_TRACKARGUMENTS = False

global PYPERF_TRACKCALLER
PYPERF_TRACKCALLER = False
    
def __handle_signal(sig, frame):
    """
    simple signal handler to disable/enable pyperf at runtime
    """
    global PYPERF
    
    if ( sig == signal.SIGUSR1 ):
        if ( PYPERF ):
            PYPERF = False
            print("Disabling PyPerf module")
        else:
            PYPERF = True
            print("Enabling PyPerf module")
    elif ( sig == signal.SIGUSR2 ):
        printreport()

# SIGUSR1 enables/disables the pyperf tracking
signal.signal(signal.SIGUSR1, __handle_signal)

# SIGUSR2 prints the current pyperf report
signal.signal(signal.SIGUSR2, __handle_signal)


def reset():
    '''
    Resets the PyPerf performance measurements and zeros out everything at this
    given point in time.
    '''
    global FUNCTIONS
    FUNCTIONS = {}

def getreport():
    '''
    Returns a the current statistics gathered by the PyPerf library at runtime.
    You can reset the stats by using the reset method.
    
    The return object looks like so: 
	    {
	     "function1" : Stats(),
	     "function2" : Stats(),
	    }
    '''
    return FUNCTIONS

def printreport():
    """
    print to stdou the pyperf report as of right now.
    """
    if len(FUNCTIONS.keys()) == 0: 
        return
    
    print("\nPyPerf Report:")
    print("=============\n")
 
    labels = ["function",
              "tot calls",
              "tot dur(ms)",
              "avg dur(ms)",
              "max dur(ms)",
              "min dur(ms)"] 
    data = []
     
    for func in FUNCTIONS:
        stats = FUNCTIONS[func]
            
        if stats.total_calls != 0:
            data.append([func,
                         str(int(stats.total_calls)),
                         str(int(stats.total_duration)),
                         str(int(stats.average_duration)),
                         str(int(stats.max_duration)),
                         str(int(stats.min_duration))
                        ])

    print tableprinter.indent([labels] + data, hasHeader=True, justify='center')

atexit.register(printreport)

class Stats(object):
    """
    statistics container object.
    """
    
    def __init__(self):
        self.total_calls = 0
        self.total_duration = 0
        self.average_duration = 0
        self.max_duration = 0
        self.min_duration = sys.maxint
        
    def update(self, duration):
        """
        update statistics information based on the duration passed as an 
        argument
        """
        self.total_duration += duration
        self.total_calls += 1
        
        if duration > self.max_duration:
            self.max_duration = duration
            
        if duration < self.min_duration:
            self.min_duration = duration
            
        self.average_duration = self.total_duration / self.total_calls

class measure(object):
    '''
    This decorator is used to label the methods that you'd like to have PyPerf
    module tracking the performance stats on. With this decorator in place at 
    the end of the test run PyPerf will print the statistics for all of the 
    FUNCTIONS that had the @meausre decorator on them.
    
    At runtime you can also call the getreport method to get the exact stats 
    at the current time, and you can use the reset to simply reset all the 
    counters back to 0.
    '''

    global PYPERF_TRACKARGUMENTS
    global PYPERF_TRACKCALLER
    global PYPERF
    global FUNCTIONS
    
    def __init__(self, function, trackarguments = False):
        self.__f = function
        self.__trackarguments = trackarguments
   
    def __call__(self, *args, **kwargs): 
        if ( PYPERF ):
            stats = None
            
            if ( PYPERF_TRACKCALLER ):
                import inspect
                key = inspect.stack()[1][3] + "->" + self.__f.__name__
            elif ( PYPERF_TRACKARGUMENTS ):
                key = self.__f.__name__ + "("
                
                for arg in args:
                    aux = None
                    
                    if type(arg) == str:
                        aux = "'" + arg + "'"
                    else:
                        aux = str(arg)
                        
                    key += aux + ","

                for kwarg in kwargs:
                    key += kwarg + ","
                
                key = key[:-1] + ")"
            else:
                key = self.__f.__name__ 
                
            if not(key in FUNCTIONS.keys()):
                stats = Stats()
                FUNCTIONS[key] = stats
            else:
                stats = FUNCTIONS[key]
           
            start = time.time()*1000
            ret = self.__f(*args, **kwargs)
            duration = (time.time() * 1000) - start
            stats.update(duration)
            
            return ret
        else:
            return self.__f(*args, **kwargs)
        
    def __get__(self, obj, type=None):
        if obj is None:
            return self
        
        new_func = self.__f.__get__(obj, type)
        return self.__class__(new_func) 
 