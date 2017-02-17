from kafka import KafkaProducer
from app import Config
import msgpack, sys
from colorama import Fore
import json

# Starting the producer
producer = None


# Try to connect to Kafka, else exits the process
def connect():
    try:
        global producer
        producer = KafkaProducer(bootstrap_servers=Config.kafkaHost,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                 request_timeout_ms=5000)
        print(Fore.GREEN + '# KafkaForword OK!' + Fore.RESET)
    except RuntimeError:
        sys.exit(Fore.RED + "Connection to Kafka failed!" + Fore.RESET)


# Publishes a message to the configured kafka server
def publish(message,topic):
    if Config.kafkaUpdates:
        producer.send(topic, message)
    else:
        # we ignore this in json mode
        pass
