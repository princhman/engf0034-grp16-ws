from paho.mqtt import client as mqtt
import random

broker = "broker.emqx.io"
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected to MQTT Broker!")
        else:
            print("failed to connect, return code", rc)
    client = mqtt.Client(client_id)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client
