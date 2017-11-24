import paho.mqtt.client as mqtt
import keys
import time
import ast

temp_value = 0
light_value = 0
flag = 0
semaphore = 0
ctr = 0

def on_message(client,userdata,message):
    global temp_value, light_value, flag, semaphore, ctr

    if message.topic==keys.tuple_data:
        ctr+=1
        print "Tuple received"
        rx_data = ast.literal_eval(message.payload.decode("utf-8"))
        light_value = float(int(rx_data[0]))
        temp_value = float(int(rx_data[2]))
        light_act = int(rx_data[1])
        temp_act = int(rx_data[3])
        print "Light Sensor Value : ",light_value/ctr
        print "Light Actuator Value : ",light_act
        print "Temperature Sensor Value : ",temp_value/ctr
        print "Temperature Actuator Value : ",temp_act
        print
        
    if message.topic==keys.tempsensor:
        curr_temp_value = float(message.payload.decode("utf-8"))/255
        temp_ctr += 1
        temp_value += curr_temp_value
        
        print "From Temperature Sensor"
        print "Value Received :",curr_temp_value
        print "Average Temperature Sensor Value : ",temp_value/temp_ctr
        print
        sval = round(temp_value/temp_ctr,3)
        client.publish(keys.avgtemp,sval)

    
    
client = mqtt.Client("mrswagle")
client.on_message = on_message
client.connect('iot.eclipse.org')
while 1:
    client.loop_start()
    client.subscribe(keys.tuple_data)
    client.subscribe(keys.flag)
    time.sleep(500)
