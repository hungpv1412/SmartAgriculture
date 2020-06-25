from __future__ import absolute_import, unicode_literals
import json
import os
import sys
import django
sys.path.append('/home/drashyn/Project/STech_Agriculture/backend/src/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

import paho.mqtt.client as mqtt
from agri.models import Report, Sensor, Device, Command

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("air_topic/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    create_report(str(msg.topic), str(msg.payload)[2:-1])


def create_report(topic, payload):
    print("Create Report "+payload)
    sensor_id = ""
    index = ""
    if ("air_topic" in topic):
        sensor_id = topic.replace("air_topic/","",1)
    elif ("ground_topic" in topic):
        sensor_id = topic.replace("ground_topic/","",1)
    else : print("nothing")
    index = payload
    print("index : "+index)
    print("sensor id : "+sensor_id)
    sensor = Sensor.objects.get(sensor_id=sensor_id)
    if(sensor!= None):
        print("Have sensor")
        report = Report(
            index=index,
            sensor=sensor
        )
        report.save()
        print(Report.objects.count())


def checkDevice(report):
    pass


def makeCommand(report_before):
    pass


def editCommand(report_after):
    pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
