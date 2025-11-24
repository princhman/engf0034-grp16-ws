import threading
import time

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))


measures = []


def print_average():
    global measures
    while True:
        time.sleep(1)
        if measures:
            print(f"Average measure: {sum(measures) / len(measures)}")
            measures = []


def on_message(client, userdata, msg):
    global measures
    try:
        measure = float(msg.payload.decode())
        measures.append(measure)
    except:
        pass


client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)

client.loop_start()

timer_thread = threading.Thread(target=print_average, daemon=True)
timer_thread.start()

sub_topic = "2025-engf0002/data/stirring"
pub_topic = "2025-engf0002/action/stirring"


wanted_rpm = "900"
client.publish(pub_topic, wanted_rpm)
client.publish(pub_topic, wanted_rpm)

client.publish(pub_topic, wanted_rpm)

client.publish(pub_topic, wanted_rpm)

client.publish(pub_topic, wanted_rpm)

print("Published message")
client.subscribe(sub_topic)
input = input("Press Enter to exit")
