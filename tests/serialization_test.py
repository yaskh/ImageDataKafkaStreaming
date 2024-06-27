import unittest
import sys
sys.path.append('../src/')
from src.utils import json_serializer
from src.kafka_consumer import json_deserializer


class TestSerialization(unittest.TestCase):

    def test_json_serializer_deserializer(self):
        """Test JSON serialize and then deserialize back to original data."""
        data = {'key': 'value', 'number': 123}
        serialized_data = json_serializer(data)
        deserialized_data = json_deserializer(serialized_data)
        self.assertEqual(data, deserialized_data)

if __name__ == '__main__':
    unittest.main()
