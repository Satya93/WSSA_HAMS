
from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)

# Load Data
dataset = numpy.loadtxt("pure_data.csv",delimiter=",")
X = dataset[:,0:2]
Y = dataset[:,2:4]
print Y
# Define Model
# Compile Model
# Fit Model
# Evaluate Model

