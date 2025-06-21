from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'api_usage',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='api_logger'
)

print("Kafka consumer started. Listening for API usage logs...\n")

for message in consumer:
    data = message.value
    print(f"[Kafka Log] Event: {data['event']}, User: {data['user']}, Path: {data['path']}")
