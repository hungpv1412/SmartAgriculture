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
import json
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
    
    index = json.loads(payload)
    # print("index : "+index)
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
        # print("report index"+str(report.index.t))
        print("device_type "+device_type)
        checkDevice(report=report,device=device,device_type=device_type)
        print("count Report"+str(Report.objects.count()))


def checkDevice(report, device, device_type):
    condition=0.0
    if (device_type=="pump"):
        condition = report.index['h']
    elif (device_type=="light"):        
        condition = report.index['t']

    print("Condition"+str(condition))

    # createCommand(report_before=report,device=device,device_type=device_type)
    
    if (condition<device.turn_on_cond)and(device.is_active==False):
            print("Create Command")
            createCommand(report, device, device_type)
    elif (condition<device.turn_off_cond)and(device.is_active==True):
            print("Update Command") 
            updateCommand(device,device_type)
    elif (condition>=device.turn_off_cond)and(device.is_active==True):
            print("Finish Command") 
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
    print("command "+command.status)
    device.is_active=True
    device.save()

    print("publish command")
    client.publish(topic=device_type+"_topic/"+device.device_id,payload="{\"t\":"+str(device.safe_time)+"}",qos=0,retain=False)
    
    print("Device Turn ON "+str(device.is_active))


def updateCommand(device, device_type):
    doing_command = Command.objects.filter(device__id=1).filter(status='create').order_by('-id')[:1]
    if (doing_command!=None):
        client.publish(topic=device_type+"_topic/"+device.device_id,payload="{\"t\":"+"30"+"}",qos=0,retain=False)
    else :
        print("Command not Found")
    # make mqtt command add active time

def finishCommand(report_after, device, device_type):
    print("device status"+str(device.is_active))
    doing_command = Command.objects.filter(device__id=1).filter(status='create').order_by('-id')[:1]
    if not doing_command : print("Query error")
    else :
        print("something")
        # print(doing_command.size())
        doing_command[0].status='finish'
        doing_command[0].report_after=report_after
        doing_command[0].save()
    
        client.publish(topic=device_type+"_topic/"+device.device_id,payload="{\"t\":86400}",qos=0,retain=False)
    
        device.is_active=False
        device.save()
        print("Device Status "+str(device.is_active))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)


