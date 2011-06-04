import unittest

import time
import random

import os
import signal

import pyperf

random.seed(time.time())

@pyperf.measure
def func1():
    time.sleep(random.random()*0.0001)
    return 1

class SignalTests(unittest.TestCase):
     
    def setUp(self): 
        pyperf.PYPERF = True
        
    def test_signal_enabling_disabling(self):
        pid = os.getpid()
        os.kill(pid, signal.SIGUSR1)
        self.assertTrue(pyperf.PYPERF, "Failed to enable pyperf with SIGUSR1.")
        os.kill(pid, signal.SIGUSR1)
        self.assertFalse(pyperf.PYPERF, "Failed to disable pyperf with SIGUSR1.")

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(SignalTests))
    