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
    """Connect to broker Mosquitto and subcribe all Sensor's Topic"""
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("air_topic/#")
    client.subscribe("ground_topic/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    """Wait the message from Subcribed Topic"""
    print("Message "+msg.topic+" "+str(msg.payload))
    create_report(str(msg.topic), str(msg.payload)[2:-1])


def create_report(topic, payload):
    """Creat Report when have Topic message"""
    # print("Create Report "+payload)
    sensor_id = ""
    index = ""
    device_type = ""

    if ("air_topic" in topic):
        sensor_id = topic.replace("air_topic/","",1)
        device_type = "light"
    elif ("ground_topic" in topic):
        sensor_id = topic.replace("ground_topic/","",1)
        device_type = "pump"
    # else : print("nothing")
    
    index = payload
    
    # print("index : "+index)
    # print("sensor id : "+sensor_id)
    
    sensor = Sensor.objects.get(sensor_id=sensor_id)
    
    
    if(sensor!= None):
        print("Have sensor")
        device = Device.objects.get(id=sensor.device_id)
        if device!=None:
            print("Decive Avaiable")
        report = Report(
            index=index,
            sensor=sensor
        )
        report.save()
        checkDevice(report,device,device_type)
        print("count Report"+Report.objects.count())


def checkDevice(report, device, device_type):
    if (device_type=="pump"):
        if (report.index.h<device.turn_on_cond)and(device.is_active==False):
            createCommand(report,device,device_type)
        elif (report.index.h>=device.turn_on_cond)and(device.is_active==True):
            finishCommand(report,device,device_type)
        # elif (report.index.h>=device.turn_off_cond)and(device.is_active==True):
        #     finishCommand(report,device.device_type)
    elif (device_type=="light"):
        if (report.index.t<device.turn_on_cond)and(device.is_active==False):
            createCommand(report,device,device_type)
        elif (report.index.t>=device.turn_off_cond)and(device.is_active==True):
            finishCommand(report,device,device_type)


def createCommand(report_before, device,device_type):
    """Create command and publish mqtt message to device topic"""
    command = Command(
        device=device,
        report_before=report_before,
        status = 1,
    )
    command.save()
    client.publish(topic=device_type+"_topic/"+device.device_id,payload="{\"t\":35}",qos=0,retain=False)
    #Make mqtt command


def updateCommand(report, device, device_type):
    pass
    #make mqtt command add active time

def finishCommand(report_after, device,device_type):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
