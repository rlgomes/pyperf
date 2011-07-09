
import unittest

from basictests import BasicTests
from signaltests import SignalTests

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SignalTests))
    suite.addTest(unittest.makeSuite(BasicTests))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite())