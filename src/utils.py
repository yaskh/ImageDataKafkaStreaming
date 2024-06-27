import base64
import json
import logging
import time
import uuid
import zlib
import numpy as np


def compress_array(array):
    """ Compress a numpy array and encode it to base64. """
    compressed_data = zlib.compress(array.tobytes())
    return base64.b64encode(compressed_data).decode('utf-8')

def json_serializer(data):
    """ Serialize data to JSON format encoded in UTF-8. """
    return json.dumps(data).encode('utf-8')


def generate_and_send_data(customer_id, producer):
    """ Generate data, compress it, and send via Kafka. """
    array_id = str(uuid.uuid4())
    creation_time = time.time()
    array = np.random.randint(0, 256, (1920, 1080, 3), dtype=np.uint8)
    compressed_array = compress_array(array)
    compressed_size = len(compressed_array) / (1024 * 1024)  # Convert bytes to megabytes
    logging.info(f"Compressed array size: {compressed_size:.2f} MB")

    message = {
        "customer_id": customer_id,
        "data": compressed_array,
        "array_id": array_id,
        "creation_time": creation_time
    }
    key = str(uuid.uuid4()).encode('utf-8')
    producer.send('data-stream', key=key, value=message)
    logging.info(f"Sent message with key {key.decode('utf-8')}")

def decompress_data(encoded_data):
    """Decompresses data from base64 and zlib compressed format."""
    decoded_data = base64.b64decode(encoded_data)
    return zlib.decompress(decoded_data)

def array_from_compressed_data(compressed_data, shape=(1920, 1080, 3)):
    """Convert compressed data to a numpy array of specified shape."""
    decompressed_data = decompress_data(compressed_data)
    return np.frombuffer(decompressed_data, dtype=np.uint8).reshape(shape)

def json_deserializer(data):
    """Deserialize JSON data from Kafka."""
    return json.loads(data.decode('utf-8'))