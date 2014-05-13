# import unittest

# test_loader = unittest.TestLoader()
# tests = test_loader.discover('./robot_results_parser', '*_test.py')
# test_runner = unittest.runner.TextTestRunner(verbosity=2)
# test_runner.run(tests)

import unittest
import test_core.robot_results_parser

suite = unittest.TestLoader()
suite = suite.loadTestsFromModule(test_core.robot_results_parser)

unittest.TextTestRunner().run(suite)