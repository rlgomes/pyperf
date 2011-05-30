import unittest

import pyperf
import time
import random

random.seed(time.time())

@pyperf.measure
def func1():
    time.sleep(random.random()*0.01)
    return 1

@pyperf.measure
def func2():
    time.sleep(random.random()*0.02)
    return 2

@pyperf.measure
def func3():
    time.sleep(random.random()*0.03)
    return 3

@pyperf.measure
def func4():
    func1()
    func2()
    return 4

@pyperf.measure
def simplefunction(arg1):
    return arg1

class BasicTests(unittest.TestCase):
   
#    def test_multiple_function_performance(self):
#        lookup = { 0: func1, 1: func2, 2: func3, 3: func4, }
#        
#        for _ in range(0,10):
#            lookup[random.randrange(0,len(lookup))]()
#            
#        print pyperf.getreport()
#        pyperf.reset()

    def test_same_function_with_different_arguments(self):
        lookup = { 0: "abcd", 1: "1234", 2: "xyz" }
                  
        
        for _ in range(0,10):
            args = lookup[random.randrange(0,len(lookup))]
            simplefunction(args)
                
if __name__ == '__main__':
    unittest.main()