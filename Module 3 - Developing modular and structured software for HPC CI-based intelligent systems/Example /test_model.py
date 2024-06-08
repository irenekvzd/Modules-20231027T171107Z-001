import unittest
from model import train_model, save_model, load_model
import pandas as pd
from sklearn.linear_model import LogisticRegression

class TestModel(unittest.TestCase):
    def test_train_model(self):
        data = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8]
        })
        target = pd.Series([0, 1, 0, 1])
        model = train_model(data, target)
        self.assertIsInstance(model, LogisticRegression)
    
    def test_save_and_load_model(self):
        model = LogisticRegression()
        save_model(model, "models/test_model.joblib")
        loaded_model = load_model("models/test_model.joblib")
        self.assertIsInstance(loaded_model, LogisticRegression)

if __name__ == "__main__":
    unittest.main()
