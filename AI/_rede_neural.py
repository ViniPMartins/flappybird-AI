import numpy as np
import math
import os

class Perceptron:

    def __init__(self, input_shape, output=1):
        self.weights = np.random.randn(input_shape,output)
        self.bias = np.random.randn(output,)
        self.parameters = np.array([self.weights, self.bias], dtype=object)
           
    def predict(self, inputs):
        summation = np.dot(inputs, self.parameters[0]) + self.parameters[1]           
        activation = [math.tanh(x) for x in summation]
        return activation
    
    def get_weights(self):
        return self.parameters
    
    def set_weights(self, new_parameters):
        self.parameters = new_parameters

    def save_params(self):
        folder_name = "checkpoint"
        file_name = "saved_params_v3.npy"

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        filepath = os.path.join(folder_name, file_name)

        np.save(filepath, self.parameters, allow_pickle=True)
        return print("Paramters saved in: ", filepath)
    
    def load_params(self):
        folder_name = "checkpoint"
        file_name = "saved_params.npy"
        filepath = os.path.join(folder_name, file_name)
        
        self.parameters = np.load(filepath, allow_pickle=True)
        return print("Paramters load")

def create_model(input_shape):
    model = Perceptron(input_shape)
    return model

def create_weights(input_shape):
    model = create_model(input_shape)
    return model.get_weights()