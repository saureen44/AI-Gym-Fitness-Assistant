import paho.mqtt.client as mqtt
import json
import time

MQTT_BROKER = "localhost"  # Or your cloud broker IP
MQTT_PORT = 1883
TOPIC_TELEMETRY = "gym/device/telemetry"
TOPIC_RECOMMENDATION = "gym/device/recommendation"

# Simulated AI logic for resistance/rest adjustment
def generate_ai_recommendation(heart_rate, exertion_level):
    if heart_rate > 160 or exertion_level > 8:
        return {"action": "decrease_resistance", "value": 15, "advice": "High intensity detected. Reduce resistance by 15% and rest for 60s."}
    elif heart_rate < 110:
        return {"action": "increase_resistance", "value": 10, "advice": "Heart rate low. Increase intensity."}
    else:
        return {"action": "maintain", "value": 0, "advice": "Optimal zone. Maintain current pace."}

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with code {rc}")
    client.subscribe(TOPIC_TELEMETRY)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    print(f"Received Telemetry: {payload}")
    
    # Process through AI
    ai_response = generate_ai_recommendation(payload['heart_rate'], payload['exertion'])
    
    # Send recommendations back via MQTT
    client.publish(TOPIC_RECOMMENDATION, json.dumps(ai_response))

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()