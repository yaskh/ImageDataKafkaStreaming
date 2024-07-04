# Image Data Streaming Application

This application demonstrates how to stream compressed image data using Apache Kafka. It includes a producer component that generates and sends compressed image data, and a consumer component that receives, decompresses, and saves the data as images.

## Installation

No additional installation is required; Docker Compose handles all necessary installations.

### Starting the Script Setup

To initiate the application, run the following command. This starts Zookeeper and Kafka, runs the tests, activates the Producer, and finally, the Consumer. The output will be saved to a local directory named `output`.

```bash
docker-compose up -d

 ```

## CLI Arguments 
**Modify the command in the docker-compose file**
### Kafka Producer

Run `data_generator.py` from the command line, specifying the desired options. Below are the available command-line arguments:

- `-bs`, `--bootstrap_servers`: Kafka bootstrap servers (default: `localhost:29092`).
- `-rt`, `--request_timeout_ms`: Kafka request timeout in milliseconds (default: `300000`).
- `-mrs`, `--max_request_size`: Kafka maximum request size in bytes (default: `13772512`).
- `-a`, `--acks`: Acknowledgments config (default: `1`).
- `-n`, `--num_messages`: Number of messages to generate and send (required).
- `-cid`, `--customer_id`: Customer ID to use in message generation (required).


### Kafka Consumer
**Modify the command in the docker-compose file**

To start the consumer, which receives, decompresses, and saves the image data, run:

- `-t`, `--topic`, default='data-stream', Kafka topic to send messages to (default: `data-stream`)
- `-bs`, `--bootstrap_servers`, default='localhost:29092', Kafka bootstrap servers (default: `localhost:29092`)
- `-aor`, `--auto_offset_reset`, default='earliest', Kafka consumer auto offset reset (default: `earliest`)
- `-eac`, `--enable_auto_commit`, default=False, Kafka consumer enable auto commit (default: `False`)
- `-gid`, `--group_id`, default='image-consumer', Kafka consumer group ID (default: `image-consumer`)
- `-o`, `--output_directory`, default='output', Output directory for saving images (default: `output`)


## Viewing the logs 
Test cases: docker-compose logs tests
Kafka Producer: docker-compose logs kafka_producer
Kafka Consumer: docker-compose logs kafka_consumer