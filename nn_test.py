import numpy as np
np.random.seed(0)

# Load Data
dataset = np.loadtxt("pure_data.csv",delimiter=",")
X = dataset[:,0:2]
Y = dataset[:,2:4]

# Metrics
nn_input_dim = 2
nn_output_dim = 2
num_examples = len(X)

# Parameters
eps = 0.01 # Learning rate for gradient descent
reg_lam = 0.01 # Regularization strength

