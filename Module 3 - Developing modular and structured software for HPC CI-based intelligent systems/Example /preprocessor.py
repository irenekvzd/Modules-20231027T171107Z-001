from sklearn.preprocessing import StandardScaler
import pandas as pd

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data by scaling the features."""
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return pd.DataFrame(scaled_data, columns=data.columns)

if __name__ == "__main__":
    data = pd.read_csv("data/sample_data.csv")
    processed_data = preprocess_data(data)
    print(processed_data.head())
