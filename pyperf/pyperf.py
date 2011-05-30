import time
import sys
import atexit

import tableprinter

global functions
functions = {}
    
global PYPERF
PYPERF = True

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
    '''
    data = {}
    
    for f in functions:
        m = functions[f]
        totaldur = m.totaldur()
            
        if  m.count() != 0 :
            count = m.count()
            avg = totaldur/count
        else:
            count = 0
            avg = 0
            
        maxdur = m.maxdur()
        mindur = m.mindur()
        
        data[f.__name__] = {"calls" : str(int(count)),
                            "totaldur" : str(int(totaldur)),
                            "avgdur" : str(int(avg)),
                            "maxdur" : str(int(maxdur)),
                            "mindur" : str(int(mindur))}
        
    return data

def __printreport():
    if len(functions.keys()) == 0: 
        return
    
    print("\nPyPerf Report:")
    print("==============\n")
 
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
            totaldur = m.totaldur()
            
            if  m.count() != 0 :
                count = m.count()
                avg = totaldur/count
            else:
                count = 0
                avg = 0
                
            maxdur = m.maxdur()
            mindur = m.mindur()
            
            if count != 0:
                data.append([f.__name__,
                             str(int(count)),
                             str(int(totaldur)),
                             str(int(avg)),
                             str(int(maxdur)),
                             str(int(mindur))])
    except Exception as e: 
        print("errnoror at exit %s" % e)

    print tableprinter.indent([labels] + data, hasHeader=True, justify='center')

atexit.register(__printreport)

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

    global PYPERF
    global functions
    
    def __init__(self, function, trackarguments = False):
        self.__f = function
        self.__count = 0
        self.__totaldur = 0
        self.__mindur = sys.maxint
        self.__maxdur = 0
        functions[function] = self
   
    def __call__(self, *args, **kwargs): 
        if ( PYPERF ):
            t = time.time()*1000
            ret = self.__f(*args, **kwargs)
            dur = (time.time() * 1000) - t
            
            self.__totaldur+=dur
            self.__count+=1
            
            if dur > self.__maxdur:
                self.__maxdur = dur

            if dur < self.__mindur:
                self.__mindur = dur
            
            return ret
        else:
            return self.__f(*args, **kwargs)

    def count(self):
        return self.__count

    def totaldur(self):
        return self.__totaldur

    def maxdur(self):
        return self.__maxdur

    def mindur(self):
        return self.__mindur
    