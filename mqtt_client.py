import paho.mqtt.client as mqtt
import keys
import time
import ast
import csv
import nn_test as nn

temp_value = 0
light_value = 0
flag = 0
semaphore = 0
ctr = 0

def on_message(client,userdata,message):
    global temp_value, light_value, flag, semaphore, ctr

    if message.topic==keys.tuple_data:
        ctr+=1
        rx_data = ast.literal_eval(message.payload.decode("utf-8"))
        light_value = round(float(int(rx_data[0]))/255,3)
        temp_value = round(float(int(rx_data[2]))/255,3)
        light_act = int(rx_data[1])
        temp_act = int(rx_data[3])
        data = [light_value,temp_value,light_act,temp_act]
        with open(r'pure_data.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        print "Light Sensor Value : ",light_value
        print "Light Actuator Value : ",light_act
        print "Temperature Sensor Value : ",temp_value
        print "Temperature Actuator Value : ",temp_act
        print "Samples : ",ctr
        print 

    if message.topic==keys.ack:
        value = int(message.payload.decode("utf-8"))
        if value == 1:
            print "Acknowledged!"
            nn.build_model(3)
            time.sleep(5)
            client.publish(keys.flag,payload = 1,qos = 2)
    
    if ctr>5:
        ctr = 0
        client.publish(keys.flag,payload = 0,qos = 2)

    return

    
    
client = mqtt.Client("mrswagle")
client.on_message = on_message
client.connect('iot.eclipse.org')
while 1:
    client.loop_start()
    client.subscribe(keys.tuple_data)
    client.subscribe(keys.ack)
    time.sleep(500)
