import unittest

test_loader = unittest.TestLoader()
tests = test_loader.discover('.', '*_test.py')
test_runner = unittest.runner.TextTestRunner(verbosity=2)
test_runner.run(tests)