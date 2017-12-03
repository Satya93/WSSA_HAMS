import nn_test as nn

out = nn.build_model(4)
model_out = out[0]
inp = [0.71,0.094]
op = nn.predict(model_out, inp)
print(op)
