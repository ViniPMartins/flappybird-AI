from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from keras.initializers import RandomNormal

def create_model(input_shape):
    model = Sequential([
        Dense(2, input_shape=(input_shape,), activation='relu', bias_initializer=RandomNormal(mean=0.0, stddev=1.0)),
        Dense(1, activation='relu', bias_initializer=RandomNormal(mean=0.0, stddev=1.0))
    ])

    return model

def create_weights(input_shape):
    model = create_model(input_shape)
    return model.get_weights()