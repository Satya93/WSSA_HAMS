import paho.mqtt.client as mqtt
import time
import keys
import random

client = mqtt.Client("mrswagle_pub")
client.connect('iot.eclipse.org')

client.loop_start()
while 1:
    light_val = random.randint(0,255)
    temp_val = random.randint(0,255)
    if light_val>80 and random.randint(0,255)>200:
        light_act = 1
    else : light_act = 0
    if temp_val>120 and random.randint(0,255)>200:
        temp_act = 1
    else : temp_act = 0
    print "Light Sensor : ",light_val
    print "Temp Sensor : ",temp_val
    data = [light_val,light_act,temp_val,temp_act]
    client.publish(keys.tuple_data,data)
    time.sleep(1)