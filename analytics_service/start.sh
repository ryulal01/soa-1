#!/bin/bash
# Запуск gRPC-сервера в фоне
python main.py &

# Запуск Kafka consumer
python kafka_consumer.py

