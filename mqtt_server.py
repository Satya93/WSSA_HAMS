import paho.mqtt.client as mqtt
import keys
import time
import ast
import csv
import nn_test as nn
import numpy as np

temp_value = 0
training_done = 0
light_value = 0
flag = 0
semaphore = 0
ctr = 0
old_cost = 0
new_cost = 0
done = 0
model_out = {}
send_tuple = [0,0,0]
rx_data = 0

data_from_light = 0
data_from_temp = 0
act_light = 0
act_temp = 0

def train():
    global send_tuple, flag, semaphore, ctr, old_cost, new_cost,rx_data, model_out, act_light, act_temp
    ctr+=1
    act_status = act_temp*2 + act_light
    send_tuple[2] = act_status

    with open(r'realworld_data.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(send_tuple)
        f.flush()
    f.close()
    print "Saved Value : ",send_tuple
    print "Done : ",done
    print "Samples : ",ctr

def on_message(client,userdata,message):
    global temp_value, light_value, flag, semaphore, ctr, old_cost, new_cost, done, rx_data, model_out, training_done, send_tuple, act_light, act_temp, data_from_light, data_from_temp
    print "New Message!"
    print message.topic
    print message.payload
    rx_data = ast.literal_eval(message.payload.decode("utf-8"))

    if message.topic==keys.node_light and training_done == 0:
        print rx_data
        send_tuple[0] = round(float(int(rx_data[0]))/1024,3)
        act_light = round(float(int(rx_data[1]))/1024,3)
        data_from_light = 1
        print "Sending Ack"
        client.publish(keys.ack,1)

    if message.topic==keys.node_temp and training_done == 0:
        send_tuple[1] = round(float(int(rx_data[0]))/1024,3)
        act_temp = round(float(int(rx_data[1]))/1024,3)
        data_from_temp = 1

    if data_from_light == 1 and data_from_temp == 1:
        data_from_light = 0
        data_from_temp = 0
        train()

    if message.topic==keys.ack and done == 0:
        print rx_data
        value = int(message.payload.decode("utf-8"))
        if value == 1:
            print "Training Neural Network"
            old_cost = new_cost
            out = nn.build_model(3)
            new_cost = float(out[1])
            model_out = out[0]
            if abs(old_cost-new_cost) < 0.02:
                done = 1
            print "Sending Key 1"
            client.publish(keys.flag,payload = 1,qos = 2)
    
    if ctr>9 and done == 0:
        ctr = 0
        print "Sending Key 0"
        client.publish(keys.flag,payload = 0,qos = 2)

    if done == 1:
        print "Neural network trained!"
        print "Sending Key 2"
        client.publish(keys.flag,payload = 2,qos = 2)
        done = 2

    if done == 2 :
        if message.topic==keys.tuple_data:
            print "Counter : ",ctr
            rx_data = ast.literal_eval(message.payload.decode("utf-8"))
            print rx_data
            light_value = round(float(int(rx_data[0]))/255,3)
            temp_value = round(float(int(rx_data[1]))/255,3)
            inp = [light_value,temp_value]
            op = nn.predict(model_out, inp)
            predc = op[0]
            print "Predicted Output is ", predc
            lgt_ot = predc%2
            temp_ot = predc/2
            inp.append(lgt_ot)
            inp.append(temp_ot)
            inp = str(inp)
            time.sleep(1)
            print "Sending Predicted Tuple"
            client.publish(keys.pred_tuple_data,inp)
            ctr = 0
        training_done = 1

    print 


    return

    
    
client = mqtt.Client("mrswagle")
client.on_message = on_message
client.connect('iot.eclipse.org')
while 1:
    client.loop_start()
    client.subscribe(keys.node_light)
    client.subscribe(keys.node_temp)
    client.subscribe(keys.ack)
    time.sleep(500)