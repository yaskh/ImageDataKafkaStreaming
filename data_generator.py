from src.KafkaProducerWrapper import KafkaProducerWrapper
from src.utils import generate_and_send_data
import logging
import json
import base64
import zlib
import argparse
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)

def compress_array(array):
    """ Compress a numpy array and encode it to base64. """
    compressed_data = zlib.compress(array.tobytes())
    return base64.b64encode(compressed_data).decode('utf-8')

def json_serializer(data):
    """ Serialize data to JSON format encoded in UTF-8. """
    return json.dumps(data).encode('utf-8')



# Set up argument parsing
parser = argparse.ArgumentParser(description='Process customer ID.')
parser.add_argument('-cid', '--customer_id', type=str, default=str(uuid.uuid4()),
                    help='Customer ID (default: generate new UUID)')
parser.add_argument('-n', '--num_messages', type=int, default=1,
                    help='Number of messages to generate (default: 1)')

parser.add_argument('-bs', '--bootstrap_servers', type=str, default='localhost:29092',
                    help='Kafka bootstrap servers (default: localhost:29092)')
parser.add_argument('-rt', '--request_timeout_ms', type=int, default=300000,
                    help='Kafka request timeout in milliseconds (default: 300000)')
parser.add_argument('-mrs', '--max_request_size', type=int, default=13772512,
                    help='Kafka maximum request size in bytes (default: 13772512)')
parser.add_argument('-a', '--acks', type=str, default=1,
                    help='Acknowledgments config (default: 1)')

args = parser.parse_args()



if __name__ == '__main__':
    producer = KafkaProducerWrapper(
        bootstrap_servers=args.bootstrap_servers,
        value_serializer=json_serializer,
        request_timeout_ms=args.request_timeout_ms,
        max_request_size=args.max_request_size,
        acks=args.acks
    )
    try:
        for i in range(args.num_messages):
            generate_and_send_data(args.customer_id, producer)
    except KeyboardInterrupt:
        logging.info("Terminated by user")
    finally:
        producer.close()