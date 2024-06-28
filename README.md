# Image Data Streaming Application

This application demonstrates the streaming of compressed image data using Apache Kafka. It includes a producer component that generates and sends compressed image data, and a consumer component that receives, decompresses, and saves the data as images.

## Prerequisites

- Apache Kafka is are accessible.
- Python 3.7+ with packages: `kafka-python`, `numpy`, `Pillow`, `zlib`, `base64`.

## Installation

### Install Required Python Packages

Run the following command to install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### Kafka and ZooKeeper Setup

To start run the command

```bash
 docker-compose up -d
 ```

## Usage

### Starting the Producer

Run `data_generator.py` from the command line, specifying the desired options. Below are the available command-line arguments:

- `-bs`, `--bootstrap_servers`: Kafka bootstrap servers (default: `localhost:29092`).
- `-rt`, `--request_timeout_ms`: Kafka request timeout in milliseconds (default: `300000`).
- `-mrs`, `--max_request_size`: Kafka maximum request size in bytes (default: `13772512`).
- `-a`, `--acks`: Acknowledgments config (default: `1`).
- `-n`, `--num_messages`: Number of messages to generate and send (required).
- `-cid`, `--customer_id`: Customer ID to use in message generation (required).

Example command:

```bash
python data_generator.py -n 10
```

### Starting the Consumer

To start the consumer, which receives, decompresses, and saves the image data, run:

- `-t`, `--topic`, default='data-stream', Kafka topic to send messages to (default: `data-stream`)
- `-bs`, `--bootstrap_servers`, default='localhost:29092', Kafka bootstrap servers (default: `localhost:29092`)
- `-aor`, `--auto_offset_reset`, default='earliest', Kafka consumer auto offset reset (default: `earliest`)
- `-eac`, `--enable_auto_commit`, default=False, Kafka consumer enable auto commit (default: `False`)
- `-gid`, `--group_id`, default='image-consumer', Kafka consumer group ID (default: `image-consumer`)
- `-o`, `--output_directory`, default='output', Output directory for saving images (default: `output`)





```bash
python src/consumer.py
```
## Running tests
To run tests, run the following command:

```bash
pytest
