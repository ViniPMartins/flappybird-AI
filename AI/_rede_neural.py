from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

def create_model(input_shape):
    model = Sequential([
        Dense(3, input_shape=(input_shape,), activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    return model