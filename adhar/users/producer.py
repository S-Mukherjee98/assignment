from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_api_usage_log(event_name, user_email=None, path=None):
    data = {
        'event': event_name,
        'user': user_email,
        'path': path,
    }
    try:
        producer.send('api_usage', data)
        producer.flush()
    except Exception as e:
        print("Kafka send error:", str(e))
