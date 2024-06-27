import os
import logging
from kafka import KafkaConsumer
from PIL import Image
from datetime import datetime
from src.utils import json_deserializer, array_from_compressed_data


logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(
    'data-stream',
    bootstrap_servers=['localhost:29092'],
    value_deserializer=json_deserializer,
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='consumer-group'
)

if __name__ == '__main__':
    for message in consumer:
        try:
            value = message.value
            output_directory = os.path.join(f'customer={value["customer_id"]}',\
                                             f'date={datetime.fromtimestamp(value["creation_time"]).strftime("%Y-%m-%d")}')
            
            file_path = os.path.join(output_directory, f'{value["array_id"]}.png')
            
            os.makedirs(output_directory, exist_ok=True)

            decompressed_array = array_from_compressed_data(value["data"])
            image = Image.fromarray(decompressed_array)
            image.save(file_path)
            
            logging.info(f"Decompressed image saved to {file_path}")
            logging.info(f"Image dimensions: {decompressed_array.shape}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
