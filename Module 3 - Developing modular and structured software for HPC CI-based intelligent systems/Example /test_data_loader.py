import unittest
from data_loader import load_data
import pandas as pd

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        data = load_data("data/sample_data.csv")
        self.assertIsInstance(data, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
