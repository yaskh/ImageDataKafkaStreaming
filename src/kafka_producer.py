from kafka import KafkaProducer
import numpy as np
import time
import uuid
import json
from data_generator import generate_image

def serialize_image(image):
    """Serialize the image array to bytes."""
    return image.tobytes()

def create_producer():
    """Create a Kafka producer."""
    return KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=serialize_image)

if __name__ == "__main__":
    producer = create_producer()
    customer_id = str(uuid.uuid4())
    while True:
        image = generate_image()
        image_id = str(uuid.uuid4())
        timestamp = time.time()
        metadata = {
            "customer_id": customer_id,
            "image_id": image_id,
            "timestamp": timestamp
        }
        producer.send('data-stream', value=image, key=bytes(json.dumps(metadata), 'utf-8'))
        print(f"Sent image {image_id} to Kafka for customer {customer_id}")
        time.sleep(1)
