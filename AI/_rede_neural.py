from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from keras.initializers import RandomNormal

def create_model(input_shape):
    model = Sequential([
        Dense(1, input_shape=(input_shape,), activation='tanh'),
        Dense(1, activation='tanh')
    ])

    return model

def create_weights(input_shape):
    model = create_model(input_shape)
    return model.get_weights()