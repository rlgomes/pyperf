import unittest

import pyperf
import time
import random

random.seed(time.time())

@pyperf.measure
def func1():
    time.sleep(random.random()*0.0001)
    return 1

@pyperf.measure
def func2():
    time.sleep(random.random()*0.0002)
    return 2

@pyperf.measure
def func3():
    time.sleep(random.random()*0.0003)
    return 3

@pyperf.measure
def func4():
    time.sleep(random.random()*0.0004)
    return 4

@pyperf.measure
def sfunc(a,b=None,c=None):
    time.sleep(random.random()*0.0001)
    return a

def cfunc1():
    func1()

def cfunc2():
    func1()

def cfunc3():
    func1()

class BasicTests(unittest.TestCase):
   
    def setUp(self): 
        pyperf.PYPERF = True
        
    def test_multiple_function_calls(self):
        ITERATIONS = 100
        pyperf.PYPERF_TRACKARGUMENTS = False
        lookup = { 0: func1, 1: func2, 2: func3, 3: func4, }
        
        for _ in range(0,ITERATIONS):
            lookup[random.randrange(0,len(lookup))]()
            
        report = pyperf.getreport()
        pyperf.printreport()
        total = 0 
        for f in report:
            total += report[f].total_calls
            
        self.assertTrue(total == ITERATIONS,
                        msg="Not all function calls were accounted for") 
        pyperf.reset()

    def test_same_function_with_different_arguments(self):
        ITERATIONS = 100
        pyperf.PYPERF_TRACKARGUMENTS = True
        try:
            for _ in range(0,ITERATIONS):
                args = random.randrange(0,3)
                if args == 0:
                    sfunc(1)
                elif args == 1: 
                    sfunc('a',2)
                elif args == 2: 
                    sfunc('a','c')
        finally:
            pyperf.PYPERF_TRACKARGUMENTS = False
            
        report = pyperf.getreport()
        pyperf.printreport()
        self.assertTrue(report["sfunc('a',2)"].total_calls > 0,
                        msg="Did not find sfunc('a',2) calls.")
        self.assertTrue(report["sfunc('a','c')"].total_calls > 0,
                        msg="Did not find sfunc('a','c') calls.")
        self.assertTrue(report["sfunc(1)"].total_calls > 0,
                        msg="Did not find sfunc(1) calls.")
        pyperf.reset()
        
    def test_same_function_with_different_callers(self):
        ITERATIONS = 100
        pyperf.PYPERF_TRACKCALLER = True
        try:
            for _ in range(0,ITERATIONS):
                args = random.randrange(0,3)
                if args == 0:
                    cfunc1()
                elif args == 1: 
                    cfunc2()
                elif args == 2: 
                    cfunc3()
        finally:
            pyperf.PYPERF_TRACKCALLER = False
           
        report = pyperf.getreport()
        pyperf.printreport()
        self.assertTrue(report["cfunc1->func1"].total_calls > 0,
                        msg="Did not find cfunc1->func1 calls.")
        self.assertTrue(report["cfunc2->func1"].total_calls > 0,
                        msg="Did not find cfunc2->func1 calls.")
        self.assertTrue(report["cfunc3->func1"].total_calls > 0,
                        msg="Did not find cfunc3->func1 calls.")
        pyperf.reset()
                
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(BasicTests))
    