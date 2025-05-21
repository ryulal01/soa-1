from kafka import KafkaProducer
import json

_producer = None

def get_kafka_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    return _producer

def send_kafka_event(topic, data):
    try:
        producer = get_kafka_producer()
        producer.send(topic, value=data)
        producer.flush()
    except Exception as e:
        print(f"[Kafka Error] Failed to send event: {e}")

