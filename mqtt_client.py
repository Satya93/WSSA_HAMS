import paho.mqtt.client as mqtt
import time

temp_value = 0
light_value = 0
flag = 0
semaphore = 0
temp_ctr = 0
light_ctr = 0

def on_message(client,userdata,message):
    global temp_value, light_value, flag, semaphore, light_ctr, temp_ctr

    if message.topic=="lightsensor/value":
        curr_light_value = float(message.payload.decode("utf-8"))/255
        light_ctr += 1
        light_value += curr_light_value
        
        print "From Light Sensor"
        print "Value Received :",curr_light_value
        print "Average Light Sensor Value : ",light_value/light_ctr
        print
        sval = round(light_value/light_ctr,3)
        client.publish('avglight/value',sval)
        
    if message.topic=="tempsensor/value":
        curr_temp_value = float(message.payload.decode("utf-8"))/255
        temp_ctr += 1
        temp_value += curr_temp_value
        
        print "From Temperature Sensor"
        print "Value Received :",curr_temp_value
        print "Average Temperature Sensor Value : ",temp_value/temp_ctr
        print
        sval = round(temp_value/temp_ctr,3)
        client.publish('avgtemp/value',sval)

    
    
client = mqtt.Client("mrswagle")
client.on_message = on_message
client.connect('iot.eclipse.org')
while 1:
    client.loop_start()
    client.subscribe('lightsensor/value')
    client.subscribe('tempsensor/value')
    client.subscribe('lightactuator/value')
    client.subscribe('tempactuator/value')
    client.subscribe('flag/value')
    time.sleep(500)
