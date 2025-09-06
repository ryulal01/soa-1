import json
from aiokafka import AIOKafkaConsumer
import asyncio
from storage import Storage
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPICS = ["post_views", "post_likes", "post_comments"]


async def consume():
    consumer = AIOKafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    storage = Storage()
    try:
        async for msg in consumer:
            event = msg.value
            event_type = None
            if msg.topic == "post_views":
                event_type = "view"
            elif msg.topic == "post_likes":
                event_type = "like"
            elif msg.topic == "post_comments":
                event_type = "comment"

            if event_type:
                # Преобразуем timestamp в datetime
                timestamp_str = event.get('timestamp')
                try:
                    event_time = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.utcnow()
                except ValueError:
                    print(f"[Consumer] Invalid timestamp format: {timestamp_str}")
                    event_time = datetime.utcnow()

                # Поддержка как client_id, так и user_id
                user_id = event.get('user_id') or event.get('client_id')

                storage.insert_event(
                    event_type=event_type,
                    post_id=str(event.get('post_id')),
                    user_id=str(user_id),
                    event_time=event_time
                )
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())

