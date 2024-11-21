from kafka import KafkaProducer
import json
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def produce_log(user_id: int, action: str):
    message = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.now().isoformat()
    }
    producer.send("logs", value=message)
