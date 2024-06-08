import unittest
import numpy as np
from hpc_utils import parallel_sum
from mpi4py import MPI

class TestHPCUtils(unittest.TestCase):
    def test_parallel_sum(self):
        data = np.arange(100)
        total_sum = parallel_sum(data)
        if MPI.COMM_WORLD.Get_rank() == 0:
            self.assertEqual(total_sum, np.sum(data))

if __name__ == "__main__":
    unittest.main()
