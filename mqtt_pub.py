import paho.mqtt.client as mqtt
import time
import keys
import random
import csv

flag = 1

def on_message(client,userdata,message):
    global flag
    value = int(message.payload.decode("utf-8"))
    if value == 0:
        print "Stopping..."
        client.publish(keys.ack,1)
        flag = 0
        return
    if value == 1:
        print "Starting..."
        client.publish(keys.ack,0)
        flag = 1
        return
    
client = mqtt.Client("mrswagle_pub")
client.on_message = on_message
client.connect('iot.eclipse.org')
client.loop_start()
client.subscribe(keys.flag)
while 1:
    if flag == 1:
        light_val = random.randint(0,255)
        temp_val = random.randint(0,255)
        if light_val>80 and random.randint(0,255)>0:
            light_act = 1
        else : light_act = 0
        if temp_val>120 and random.randint(0,255)>0:
            temp_act = 1
        else : temp_act = 0
        print "Light Sensor : ",light_val
        print "Temp Sensor : ",temp_val
        print 
        data = str([light_val,light_act,temp_val,temp_act])
        client.publish(keys.tuple_data,data)
    time.sleep(2)