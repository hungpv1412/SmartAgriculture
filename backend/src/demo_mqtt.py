from __future__ import absolute_import, unicode_literals
import json
import os
import sys
import django
sys.path.append('/home/drashyn/workspace/SmartAgriculture/backend/src/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

import paho.mqtt.client as mqtt
from agri.models import Report, Sensor, Device, Command

def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("air_topic/#")
    client.subscribe("ground_topic/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print("Message "+msg.topic+" "+str(msg.payload))
    create_report(str(msg.topic), str(msg.payload)[2:-1])

def create_report(topic, payload):
    print("Create Report "+payload)
    sensor_topic_id = ""
    index = ""
    device_type = ""

    if ("air_topic" in topic):
        sensor_topic_id = topic.replace("air_topic/","",1)
        device_type = "light"
        print(device_type)
    elif ("ground_topic" in topic):
        sensor_topic_id = topic.replace("ground_topic/","",1)
        device_type = "pump"
        print(device_type)
    else : 
        print("nothing")
    
    index = payload
    print("index : "+index)
    print("sensor topic id : "+sensor_topic_id)
    print("sensor count "+str(Sensor.objects.count()))
    sensor = Sensor.objects.get(sensor_id=sensor_topic_id)
    print("Have sensor and device id "+str(sensor.id))
    
    if(sensor!= None):
        device = Device.objects.get(pk=sensor.device_id)
        report = Report(
            index=index,
            sensor=sensor,
        )
        report.save()
        print("report id "+str(report.id))
        print("device_type "+device_type)
        checkDevice(report=report,device=device,device_type=device_type)
        print("count Report"+str(Report.objects.count()))


def checkDevice(report, device, device_type):
    condition=""
    if (device_type=="pump"):
        condition = report.index
    elif (device_type=="light"):        
        condition = report.index

    print(condition)

    createCommand(report_before=report,device=device,device_type=device_type)
    
    if (condition<device.turn_on_cond):
            if device.is_active==False:
                createCommand(report, device, device_type)
            else : 
                updateCommand(device,device_type)
    elif (condition>=device.turn_on_cond)and(device.is_active==True):
            finishCommand(report,device,device_type)



def createCommand(report_before, device,device_type):
    print("Report id "+str(report_before.id)+" device id "+device.device_id)
    command = Command(
        device=device,
        report_before=report_before,
        report_after=report_before,
        status = 'create'
    )
    command.save()
    print("publish command")
    client.publish(topic=device_type+"_topic/"+device.device_id,payload="{\"t\":"+str(device.safe_time)+"}",qos=0,retain=False)
    #Make mqtt command


def updateCommand(device, device_type):
    doing_command = Command.objects.filter(device=device).filter(status='holding').limit(1)
    
    #make mqtt command add active time

def finishCommand(report_after, device, device_type):
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
