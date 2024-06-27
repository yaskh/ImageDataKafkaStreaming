import numpy as np
import unittest
import sys
import os

# Add the 'src' folder to the Python path
sys.path.append(os.path.abspath('src'))

from data_generator import compress_array
from utils import decompress_data



class TestCompression(unittest.TestCase):

    def test_compress_decompress(self):
        """Test that an array can be compressed and then decompressed to its original form."""
        original_array = np.random.randint(0, 256, (1920, 1080, 3), dtype=np.uint8)
        compressed_data = compress_array(original_array)
        decompressed_data = decompress_data(compressed_data)
        result_array = np.frombuffer(decompressed_data, dtype=np.uint8).reshape(original_array.shape)
        np.testing.assert_array_equal(original_array, result_array)

if __name__ == '__main__':
    unittest.main()
