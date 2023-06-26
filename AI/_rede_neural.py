from tensorflow import keras

def create_model(input_shape):
    model = keras.Sequential([
        keras.layers.Dense(16, input_shape=(input_shape,), activation='relu'),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model