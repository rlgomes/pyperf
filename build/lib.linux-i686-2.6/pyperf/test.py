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

lookup = { 0: func1, 1: func2, 2: func3, 3: func4, }
for i in range(0,10):
    lookup[random.randrange(0,len(lookup))]()
        