from logging import error

from kafka import KafkaConsumer
from kafka import KafkaProducer
from app import Config
import msgpack, sys
from colorama import Fore
import json

# Starting the producer
consumer = None


# Try to connect to Kafka, else exits the process
def connect():
    try:
        global consumer
        consumer = KafkaConsumer(bootstrap_servers=Config.kafkaHost,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 group_id=None,
                                 consumer_timeout_ms=100)
        consumer.subscribe([Config.kafkaCommandsTopic])
        print(Fore.GREEN + '# KafkaConnector OK!' + Fore.RESET)
    except RuntimeError:
        sys.exit(Fore.RED + "Connection to Kafka failed!" + Fore.RESET)


# checks if we got a new configuration from the server
def checkForNewConfiguration():
    if Config.kafkaUpdates:
        try:
            # @todo get last value
            return next(consumer).value
        except:
            return None
    else:
        return None