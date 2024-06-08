from data_loader import load_data
from preprocessor import preprocess_data
from model import train_model, save_model
from hpc_utils import parallel_sum
import pandas as pd

def main():
    # Load and preprocess the data
    data = load_data("data/sample_data.csv")
    target = data.pop("target")
    processed_data = preprocess_data(data)
    
    # Train the model
    model = train_model(processed_data, target)
    save_model(model, "models/logistic_model.joblib")
    
    # Example of HPC utility
    data_array = processed_data.to_numpy().flatten()
    total_sum = parallel_sum(data_array)
    if MPI.COMM_WORLD.Get_rank() == 0:
        print(f"Total Sum: {total_sum}")

if __name__ == "__main__":
    main()
