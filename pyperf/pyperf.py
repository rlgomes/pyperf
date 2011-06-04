import time
import sys
import atexit
import signal

import tableprinter

global functions
functions = {}

global PYPERF_TRACKARGUMENTS
PYPERF_TRACKARGUMENTS = False

global PYPERF_TRACKCALLER
PYPERF_TRACKCALLER = False
    
global PYPERF
PYPERF = False

def handle_signal(sig, frame):
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
signal.signal(signal.SIGUSR1, handle_signal)

# SIGUSR2 prints the current pyperf report
signal.signal(signal.SIGUSR2, handle_signal)


def reset():
    '''
    Resets the PyPerf performance measurements and zeros out everything at this
    given point in time.
    '''
    global functions
    functions = {}

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
    return functions

def printreport():
    if len(functions.keys()) == 0: 
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
     
    try:
        for f in functions:
            m = functions[f]
            
            if m.total_calls != 0:
                data.append([f,
                             str(int(m.total_calls)),
                             str(int(m.total_duration)),
                             str(int(m.average_duration)),
                             str(int(m.max_duration)),
                             str(int(m.min_duration))
                            ])
    except Exception as e: 
        print("errnoror at exit %s" % e)

    print tableprinter.indent([labels] + data, hasHeader=True, justify='center')

atexit.register(printreport)

class Stats(object):
    
    def __init__(self):
        self.total_calls = 0
        self.total_duration = 0
        self.average_duration = 0
        self.max_duration = 0
        self.min_duration = sys.maxint
        
    def update(self,duration):
        self.total_duration+=duration
        self.total_calls+=1
        
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
    functions that had the @meausre decorator on them.
    
    At runtime you can also call the getreport method to get the exact stats 
    at the current time, and you can use the reset to simply reset all the 
    counters back to 0.
    '''

    global PYPERF_TRACKARGUMENTS
    global PYPERF_TRACKCALLER
    global PYPERF
    global functions
    
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
                
                for a in args:
                    aux = None
                    
                    if type(a) == str:
                        aux = "'" + a + "'"
                    else:
                        aux = str(a)
                        
                    key += aux + ","

                for k in kwargs:
                    key += k + ","
                
                key = key[:-1] + ")"
            else:
                key = self.__f.__name__ 
                
            if not(key in functions.keys()):
                stats = Stats()
                functions[key] = stats
            else:
                stats = functions[key]
           
            t = time.time()*1000
            ret = self.__f(*args, **kwargs)
            duration = (time.time() * 1000) - t
            stats.update(duration)
            
            return ret
        else:
            return self.__f(*args, **kwargs)
    