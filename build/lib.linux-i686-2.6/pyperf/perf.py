import time
import atexit

global functions
functions = {}
    
global DEBUG
DEBUG = True

def printperformance():
    try:
        for f in functions:
            m = functions[f]
            if  m.count() != 0 :
                print("%s called %d times with avg %dms" % \
                      (f.__name__,m.count(),m.totaldur()/m.count()))
    except Exception as e: 
        print("Error at exit %s" % e)

atexit.register(printperformance)

class measure(object):

    global DEBUG
    global functions
    
    def __init__(self, function):
        self.__f = function
        self.__count = 0
        self.__totaldur = 0
        functions[function] = self
   
    def __call__(self, *args, **kwargs): 
        if ( DEBUG ):
            t = time.time()*1000
            ret = self.__f(*args, **kwargs)
            dur = (time.time() * 1000) - t
            
            self.__totaldur+=dur
            self.__count+=1
            
            return ret
        else:
            return self.__f(*args, **kwargs)

    def count(self):
        return self.__count

    def totaldur(self):
        return self.__totaldur
    