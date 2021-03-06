import paho.mqtt.client as paho
import matplotlib.pyplot as plt
import numpy as np
import time

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your ip
host = "localhost"
topic = "velocity"

Fs = 40.0;  # sampling rate
Ts = 4.0/Fs; # sampling interval
t1 = np.arange(0,4,Ts)
v = np.arange(0,4,Ts)


# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

i = 0
def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");
    global v
    global i
    v[i] = msg.payload
    i = i + 1
    print(i)
    if i == 40:
        plt.plot(t1, v, color="blue")
        plt.xlim(0, 4)
        plt.xlabel('Time')
        plt.ylabel('velocity')
        plt.show()

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)


# Loop forever, receiving messages
mqttc.loop_forever()
