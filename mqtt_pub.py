import paho.mqtt.client as mqtt
import time
import keys
import random
import csv
import ast

flag = 1
value = 1
training_done = 0

def on_message(client,userdata,message):
    print "New Message!"
    print message.topic
    print message.payload
    global flag, value, training_done

    if message.topic==keys.flag:
        value = int(message.payload.decode("utf-8"))
        if value == 0:
            print "Stopping..."
            print "Send Ack 1"
            client.publish(keys.ack,1)
            flag = 0
            return
        if value == 1:
            print "Starting..."
            print "Send Ack 0"
            client.publish(keys.ack,0)
            flag = 1
            return
        if value == 2:
            print "Training Done!"
            training_done = 1
    
    if message.topic == keys.pred_tuple_data and training_done== 1:
        print "Received Predicted Values"
        rx_data = ast.literal_eval(message.payload.decode("utf-8"))
        value = 1
        print "Predicted Light Sensor Value : ",rx_data[2]
        print "Predicted Temp Sensor Value : ",rx_data[3]
        print 
        
    
client = mqtt.Client("mrswagle_pub")
client.on_message = on_message
client.connect('iot.eclipse.org')
client.loop_start()
client.subscribe(keys.flag)
client.subscribe(keys.tuple_data)
client.subscribe(keys.pred_tuple_data)
while 1:
    if flag == 1 and value > 0 and training_done == 0:
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
        data = str([light_val,temp_val,light_act,temp_act])
        print "Sending Sensed Tuple"
        print 
        client.publish(keys.tuple_data,data)
    if flag == 1 and value > 0 and training_done == 1:
        light_val = random.randint(0,255)
        temp_val = random.randint(0,255)
        light_act = "NA"
        temp_act = "NA"
        data = str([light_val,temp_val,light_act,temp_act])
        print "Publishing data to be tested"
        value = 0
        client.publish(keys.tuple_data,data)
    time.sleep(1)