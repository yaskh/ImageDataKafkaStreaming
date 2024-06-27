import logging
from kafka import KafkaProducer

class KafkaProducerWrapper:
    """ Kafka producer wrapper to send messages with acknowledgment. """
    def __init__(self, bootstrap_servers, value_serializer, request_timeout_ms, max_request_size, acks):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=value_serializer,
            request_timeout_ms=request_timeout_ms,
            max_request_size=max_request_size,
            acks=acks
        )

    def on_send_success(self, record_metadata):
        logging.info(f"Message delivered to {record_metadata.topic} [{record_metadata.partition}] @ offset {record_metadata.offset}")

    def on_send_error(self, excp):
        logging.error('Failed to deliver message', exc_info=excp)

    def send(self, topic, key, value):
        logging.info("Sending message to Kafka...")
        try:
            self.producer.send(topic, key=key, value=value).add_callback(self.on_send_success).add_errback(self.on_send_error)
        except Exception as e:
            raise e
        self.producer.flush()

    def close(self):
        self.producer.close()