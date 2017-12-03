import paho.mqtt.client as mqtt
import keys
import time
import ast
import csv
import nn_test as nn
import numpy as np

temp_value = 0
light_value = 0
flag = 0
semaphore = 0
ctr = 0
old_cost = 0
new_cost = 0
done = 0
model_out = {}
rx_data = 0

def train():
    global temp_value, light_value, flag, semaphore, ctr, old_cost, new_cost,rx_data, model_out
    ctr+=1
    light_value = round(float(int(rx_data[0]))/255,3)
    temp_value = round(float(int(rx_data[1]))/255,3)
    light_act = int(rx_data[2])
    temp_act = int(rx_data[3])
    act_status = temp_act*2 + light_act
    
    data = [light_value,temp_value,act_status]
    with open(r'pure_data_temp.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        f.flush()
    f.close()
    print "Light Sensor Value : ",light_value
    print "Light Actuator Value : ",light_act
    print "Temperature Sensor Value : ",temp_value
    print "Temperature Actuator Value : ",temp_act
    #print "Samples : ",ctr

def on_message(client,userdata,message):
    global temp_value, light_value, flag, semaphore, ctr, old_cost, new_cost, done, rx_data, model_out
    rx_data = ast.literal_eval(message.payload.decode("utf-8"))

    if message.topic==keys.tuple_data:
        train()

    if message.topic==keys.ack and done == 0:
        value = int(message.payload.decode("utf-8"))
        if value == 1:
            print "Training Neural Network"
            old_cost = new_cost
            out = nn.build_model(3)
            new_cost = float(out[1])
            model_out = out[0]
            if abs(old_cost-new_cost) < 0.02:
                done = 1
            client.publish(keys.flag,payload = 1,qos = 2)
    
    if ctr>90 and done == 0:
        ctr = 0
        client.publish(keys.flag,payload = 0,qos = 2)

    if done == 1:
        print "Neural network trained!"
        client.publish(keys.flag,payload = 2,qos = 2)
        rx_data = ast.literal_eval(message.payload.decode("utf-8"))
        inp = [light_value,temp_value]
        op = nn.predict(model_out, inp)
        print "Predicted Output is ", op[0]
        inp.append(op[0])
        inp = str(inp)
        time.sleep(1)
        client.publish(keys.tuple_data,inp)

    print 


    return

    
    
client = mqtt.Client("mrswagle")
client.on_message = on_message
client.connect('iot.eclipse.org')
while 1:
    client.loop_start()
    client.subscribe(keys.tuple_data)
    client.subscribe(keys.ack)
    time.sleep(500)