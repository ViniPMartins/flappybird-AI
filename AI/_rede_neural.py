from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from keras.initializers import RandomNormal

def create_model(input_shape):
    model = Sequential([
        Dense(4, input_shape=(input_shape,), activation='relu'),
        Dense(2, activation='relu')
    ])

    return model

def create_weights(input_shape):
    model = create_model(input_shape)
    return model.get_weights()