from sklearn.linear_model import LogisticRegression
import pandas as pd
from joblib import dump, load

def train_model(data: pd.DataFrame, target: pd.Series) -> LogisticRegression:
    """Train a logistic regression model."""
    model = LogisticRegression()
    model.fit(data, target)
    return model

def save_model(model: LogisticRegression, file_path: str):
    """Save the trained model to a file."""
    dump(model, file_path)

def load_model(file_path: str) -> LogisticRegression:
    """Load a trained model from a file."""
    return load(file_path)

if __name__ == "__main__":
    data = pd.read_csv("data/sample_data.csv")
    target = data.pop("target")
    model = train_model(data, target)
    save_model(model, "models/logistic_model.joblib")
