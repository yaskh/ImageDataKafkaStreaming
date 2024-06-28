import os
import logging
from kafka import KafkaConsumer
from PIL import Image
from datetime import datetime
from utils import json_deserializer, array_from_compressed_data
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)


parser = argparse.ArgumentParser(description='Process Kafka messages and save decompressed images.')


parser.add_argument('-t', '--topic', type=str, default='data-stream',
                    help='Kafka topic to send messages to (default: data-stream)')
parser.add_argument('-bs', '--bootstrap_servers', type=str, default='localhost:29092',
                    help='Kafka bootstrap servers (default: localhost:29092)')
parser.add_argument('-aor', '--auto_offset_reset', type=str, default='earliest',
                    help='Kafka consumer auto offset reset (default: earliest)')
parser.add_argument('-eac', '--enable_auto_commit', type=bool, default=False,
                    help='Kafka consumer enable auto commit (default: False)')
parser.add_argument('-gid', '--group_id', type=str, default='image-consumer',
                    help='Kafka consumer group ID (default: image-consumer)')
parser.add_argument('-o', '--output_directory', type=str, default='output',
                    help='Output directory for saving images (default: output)')


args = parser.parse_args()


consumer = KafkaConsumer(
    args.topic,
    bootstrap_servers=[args.bootstrap_servers],
    value_deserializer=json_deserializer,
    auto_offset_reset=args.auto_offset_reset,
    enable_auto_commit=args.enable_auto_commit,
    group_id=args.group_id
)

if __name__ == '__main__':
    for message in consumer:
        try:
            value = message.value
            output_directory = args.output_directory
            output_file_path = os.path.join(f'customer={value["customer_id"]}', 
                                            f'date={datetime.fromtimestamp(value["creation_time"]).strftime("%Y-%m-%d")}')
            output_directory = os.path.join(output_directory, output_file_path)
            
            file_path = os.path.join(output_directory, f'{value["array_id"]}.png')
            
            os.makedirs(output_directory, exist_ok=True)

            decompressed_array = array_from_compressed_data(value["data"])
            image = Image.fromarray(decompressed_array)
            image.save(file_path)
            
            logging.info(f"Decompressed image saved to {file_path}")
            logging.info(f"Image dimensions: {decompressed_array.shape}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
