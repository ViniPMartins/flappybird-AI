from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, InputLayer
from keras.initializers import RandomNormal

def create_model(input_shape):
    model = Sequential([
        InputLayer(input_shape=(input_shape,)),
        Dense(1, activation='tanh', bias_initializer=RandomNormal(0,1))
    ])

    return model

def create_weights(input_shape):
    model = create_model(input_shape)
    return model.get_weights()