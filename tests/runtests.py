#!/path/to/python/3

"""Loads all unittest.TestCase subclasses from `tests.py` and runs
all of them, or the ones specified in the input parameter list, if
present."""

import importlib
import argparse
import unittest

# Using a similar __dir__ walking procedure as badbacked.services's
# __init__.py module, identify all the TestCase subclasses in the
# tests.py module

tests_module = importlib.import_module("tests")
test_subclasses = dict((name, obj) for name, obj in 
                       tests_module.__dict__.items() if
                       type(obj) == type(object) and
                       obj != unittest.TestCase and 
                       issubclass(obj, unittest.TestCase))

# still nice to make sure this is being run as main, though I cant
# imagine why anyone would want to import it
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('selected_classes', metavar="subclass", type=str, 
                        nargs="*", help="list of TestCase subclasses to run")
    args = parser.parse_args()

    suite = unittest.TestSuite()
    for tc in test_subclasses:
        if not len(args.selected_classes) or tc in args.selected_classes:
            suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_subclasses[tc]))

    unittest.TextTestRunner().run(suite)
