import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    data = pd.read_csv(file_path)
    return data

if __name__ == "__main__":
    data = load_data("data/sample_data.csv")
    print(data.head())
