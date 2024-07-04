import sys
import os
sys.path.append(os.path.abspath('src'))

import unittest
from unittest.mock import patch
from kafka import KafkaProducer
from src.KafkaProducerWrapper import KafkaProducerWrapper

class TestKafkaProducerWrapper(unittest.TestCase):
    @patch.object(KafkaProducer, 'send')
    @patch.object(KafkaProducer, 'flush')
    def test_send_fail(self, mock_flush, mock_send):
        # Arrange
        mock_send.side_effect = Exception("Simulated send failure")
        bootstrap_servers = 'kafka:9092'
        value_serializer = lambda v: v.encode('utf-8')
        request_timeout_ms = 1000
        max_request_size = 1048576
        acks = 'all'
        
        kafka_wrapper = KafkaProducerWrapper(
            bootstrap_servers,
            value_serializer,
            request_timeout_ms,
            max_request_size,
            acks
        )
        
        topic = 'test_topic'
        key = b'test_key'
        value = 'test_value'
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            kafka_wrapper.send(topic, key, value)
        
        self.assertEqual(str(context.exception), 'Simulated send failure')
        mock_send.assert_called_once_with(topic, key=key, value=value)
        mock_flush.assert_not_called()  # flush should not be called if send raises an exception

if __name__ == '__main__':
    unittest.main()