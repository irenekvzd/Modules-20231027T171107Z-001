from mpi4py import MPI
import numpy as np

def parallel_sum(data: np.ndarray) -> float:
    """Sum an array of data in parallel using MPI."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Split the data among processes
    local_data = np.array_split(data, size)[rank]
    local_sum = np.sum(local_data)

    # Gather the local sums and calculate the total sum
    total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)
    
    return total_sum

if __name__ == "__main__":
    data = np.arange(1000)
    total_sum = parallel_sum(data)
    if MPI.COMM_WORLD.Get_rank() == 0:
        print(f"Total Sum: {total_sum}")
