from operator import sub

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()} on topic {msg.topic}")


client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)

client.loop_start()
sub_topic = "2025-engf0002/data/stirring"
pub_topic = "2025-engf0002/action/stirring"

client.publish(pub_topic, "{hello there}")
print("Published message")
client.subscribe(sub_topic)
input = input("Press Enter to exit")
