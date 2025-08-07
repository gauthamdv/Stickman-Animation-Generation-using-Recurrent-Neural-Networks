import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ReduceLROnPlateau
import numpy as np
import os

class RNNModel:
    def __init__(self, sequence_length=20, input_shape=(20, 11, 2)):
        self.sequence_length = sequence_length
        self.input_shape = input_shape
        self.model = self.create_model()

    def create_model(self):
        model = models.Sequential()
        model.add(layers.Reshape((self.sequence_length, 22), input_shape=self.input_shape))
        model.add(layers.LSTM(128, return_sequences=True))
        model.add(layers.TimeDistributed(layers.Dense(64, activation='relu')))
        model.add(layers.TimeDistributed(layers.Dense(32, activation='relu')))
        model.add(layers.TimeDistributed(layers.Dense(22)))
        model.add(layers.Reshape((self.sequence_length, 11, 2)))
        return model

    def pointwise_mse(self, y_true, y_pred):
        error = tf.square(y_true - y_pred)
        return tf.reduce_mean(error, axis=-1)

    def compile(self):
        self.model.compile(optimizer='adam', loss=self.pointwise_mse)

    def fit(self, X, y, epochs=300, reduce_lr_callback=None):
        self.model.fit(X, y, epochs=epochs, callbacks=[reduce_lr_callback])

    def save(self, model_path):
        self.model.save(model_path)
        print(f"Model saved as '{model_path}'")

    def load(self, model_path):
        if os.path.exists(model_path):
            print("Loading existing model...")
            self.model = models.load_model(model_path, custom_objects={'pointwise_mse': self.pointwise_mse})

    def summary(self):
        self.model.summary()

class DataProcessor:
    @staticmethod
    def create_sequences(data, seq_length=20):
        xs = []
        ys = []
        for i in range(len(data) - seq_length - 1):
            x = data[i:(i + seq_length)]
            y = data[(i + 1):(i + seq_length + 1)]
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys)

def main():
    data = np.load('points.npy')
    model_path = 'rnn_model.h5'

    data_processor = DataProcessor()
    X, y = data_processor.create_sequences(data)

    rnn_model = RNNModel(sequence_length=20)
    rnn_model.load(model_path)
    rnn_model.summary()

    rnn_model.compile()

    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-20)

    rnn_model.fit(X, y, epochs=300, reduce_lr_callback=reduce_lr)

    rnn_model.save(model_path)
    
if __name__ == "__main__":
    main()
