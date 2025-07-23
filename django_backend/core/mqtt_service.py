import paho.mqtt.publish as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883

def publish_to_mqtt(topic, payload):
    try:
        mqtt.single(
            topic,
            payload=json.dumps(payload),
            hostname=MQTT_BROKER,
            port=MQTT_PORT
        )
        print(f"Publicado no MQTT: {topic} | {payload}")
    except Exception as e:
        print(f"Erro MQTT: {str(e)}")