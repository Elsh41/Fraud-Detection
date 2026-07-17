import unittest
import numpy as np
import pandas as pd
from src.processing import ip_to_int

class TestProcessingMethods(unittest.TestCase):

    def test_ip_to_int_conversion(self):
        # Valid test IP
        self.assertEqual(ip_to_int("120.0.0.1"), 2013265921)
        # Handle NA values
        self.assertTrue(np.isnan(ip_to_int(np.nan)))

if __name__ == '__main__':
    unittest.main()