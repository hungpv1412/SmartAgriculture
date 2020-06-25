import paho.mqtt.client as mqtt

import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    if rc==0 :
        print("client is not connected")
    client.subscribe("$SYS/#")
    client.subscribe("#")

def on_message(client, userdata, msg):
    # Do something
    print(msg)
    # logger.error('message : '+msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("localhost", 1883, 60)
# client.loop_forever()
