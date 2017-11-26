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

np.random.seed(0)

# Load Data
dataset = np.loadtxt("pure_data.csv",delimiter=",")
X = np.array(dataset[:,0:2])
y = np.array(dataset[:,2:3])
y = y.reshape(1,len(y))
y = y[0]
y = y.astype(int)

#X,y = sklearn.datasets.make_moons(200, noise = 0.20)

# Metrics
nn_input_dim = 2
nn_output_dim = 2
num_examples = len(X)

# Parameters
eps = 0.005 # Learning rate for gradient descent
reg_lam = 0.01 # Regularization strength

def calculate_loss(model):
    global dataset,X,y

    nn_input_dim = 2
    nn_output_dim = 2
    num_examples = len(X)

    # Parameters
    eps = 0.005 # Learning rate for gradient descent
    reg_lam = 0.01 # Regularization strength

    W1,b1,W2,b2 = model['W1'],model['b1'],model['W2'],model['b2']

    # Forward propogation
    z1 = X.dot(W1)+b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2)+b2
    exp_scores = np.exp(z2)
    probs = exp_scores/np.sum(exp_scores, axis = 1, keepdims = True)

    # Calculate Loss
    correct_logprobs = -np.log(probs[range(num_examples),y])
    data_loss = np.sum(correct_logprobs)

    #Regularize Loss
    data_loss = reg_lam/2*(np.sum(np.square(W1)) + np.sum(np.square(W2)))
    return 1./(num_examples*data_loss)

# Predict Output
def predict(model, x):
    global dataset,X,y
    nn_input_dim = 2
    nn_output_dim = 2
    num_examples = len(X)

    # Parameters
    eps = 0.005 # Learning rate for gradient descent
    reg_lam = 0.01 # Regularization strength

    np.random.seed(0)

    # Load Data
    X = np.array(dataset[:,0:2])
    y = np.array(dataset[:,2:3])
    y = y.reshape(1,len(y))
    y = y[0]
    y = y.astype(int)

    W1,b1,W2,b2 = model['W1'],model['b1'],model['W2'],model['b2']
    x = np.array(x)
    # Forward propogation
    z1 = x.dot(W1)+b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2)+b2
    a2 = np.tanh(z2)
    exp_scores = np.exp(z2)
    probs = exp_scores/np.sum(exp_scores, axis = 1, keepdims = True)

    #return np.argmax(probs, axis = 1)
    return probs

# This function learns parameters for the neural network and returns the model.
# - nn_hdim: Number of nodes in the hidden layer
# - num_passes: Number of passes through the training data for gradient descent
# - print_loss: If True, print the loss every 1000 iterations
def build_model(nn_hdim, num_passes=20000, print_loss=True):
    global dataset,X,y

    dataset = np.loadtxt("pure_data.csv",delimiter=",")
    X = np.array(dataset[:,0:2])
    y = np.array(dataset[:,2:3])
    y = y.reshape(1,len(y))
    y = y[0]
    y = y.astype(int)

    nn_input_dim = 2
    nn_output_dim = 2
    num_examples = len(X)

    # Parameters
    eps = 0.005 # Learning rate for gradient descent
    reg_lam = 0.01 # Regularization strength


    # Initialize the parameters to random values. We need to learn these.
    np.random.seed(0)
    W1 = np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)
    b1 = np.zeros((1, nn_hdim))
    W2 = np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim)
    b2 = np.zeros((1, nn_output_dim))
 
    # This is what we return at the end
    model = {}
     
    # Gradient descent. For each batch...
    for i in xrange(0, num_passes):
 
        # Forward propagation
        z1 = X.dot(W1) + b1
        a1 = np.tanh(z1)
        z2 = a1.dot(W2) + b2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
 
        # Backpropagation
        delta3 = probs
        delta3[range(num_examples), y] -= 1
        dW2 = (a1.T).dot(delta3)
        db2 = np.sum(delta3, axis=0, keepdims=True)
        delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
        dW1 = np.dot(X.T, delta2)
        db1 = np.sum(delta2, axis=0)
 
        # Add regularization terms (b1 and b2 don't have regularization terms)
        dW2 += reg_lam * W2
        dW1 += reg_lam * W1
 
        # Gradient descent parameter update
        W1 += -eps * dW1
        b1 += -eps * db1
        W2 += -eps * dW2
        b2 += -eps * db2
         
        # Assign new parameters to the model
        model = { 'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
         
        # Optionally print the loss.
        # This is expensive because it uses the whole dataset, so we don't want to do it too often.
          
    print "Loss after iteration %i: %f" %(i, calculate_loss(model))
    return [model,calculate_loss(model)]

# model = build_model(3)
# Plot the decision boundary
#plot_decision_boundary(lambda x: predict(model, x))
# plt.title("Decision Boundary for hidden layer size 3")
# X_in = np.array([0.8,0])
# print predict(model,X_in)

def on_message(client,userdata,message):
    global temp_value, light_value, flag, semaphore, ctr, old_cost, new_cost 

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
            f.flush()
        f.close()
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
            old_cost = new_cost
            out = build_model(3)
            new_cost = float(out[1])
            if abs(old_cost-new_cost) < 0.002:
                print "Neural network trained!"
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