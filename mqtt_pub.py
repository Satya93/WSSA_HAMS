import paho.mqtt.client as mqtt
import time
import keys
import random

client = mqtt.Client("mrswagle_pub")
client.connect('iot.eclipse.org')

client.loop_start()
while 1:
    light_val = random.randint(0,255)
    client.publish(keys.lightsensor,light_val)
    print "Light Sensor : ",light_val
    time.sleep(1)
    temp_val = random.randint(0,255)
    client.publish(keys.tempsensor,temp_val)
    print "Temp Sensor : ",temp_val
    time.sleep(1)