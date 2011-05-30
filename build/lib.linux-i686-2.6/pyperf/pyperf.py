import time
import sys
import atexit

import tableprinter

global functions
functions = {}
    
global PYPERF
PYPERF = True

def __printreport():
    
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

    global PYPERF
    global functions
    
    def __init__(self, function):
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
    