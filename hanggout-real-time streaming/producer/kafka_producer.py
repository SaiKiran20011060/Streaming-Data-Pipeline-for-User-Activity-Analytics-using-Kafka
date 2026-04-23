from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = "hanggout-topic"

def send_to_kafka(data):
    print("Sending to Kafka:", data)
    producer.send(TOPIC, value=data)