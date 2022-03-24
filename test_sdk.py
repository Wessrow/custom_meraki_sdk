#!/usr/bin/env python

"""
Unittests
Written by Gustav Larsson
"""

import os
import sys
import unittest
from meraki_functions import MerakiSDK
from logging_handler import LogHandler

logging = LogHandler("Unittest")

try:
    api_key = os.environ["meraki_key"]
except KeyError:
    logging.format_logs(40, "FatalError", "No API-key found - Check envvars")
    sys.exit(1)

MERAKI = MerakiSDK(api_key)

class TestMerakiSDK(unittest.TestCase):
    """
    Unit tests for Meraki SDK
    """

    def test_key(self):
        """ Asserts meraki_key is properly passed """

        self.assertTrue(api_key)

    def test_valid_key(self):

        

if __name__ == "__main__":

    unittest.main()