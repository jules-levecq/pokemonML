import tensorflow as tf

print("TensorFlow is successfully installed!")
print("Version:", tf.__version__)

# create a simple tensor
tensor = tf.constant([[1.0, 2.0], [3.0, 4.0]])
print("\nTensor:")
print(tensor)

# Small test
print("\nResult of an addition:")
print(tensor + 5)

# Simple test model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(2, activation='relu'),
    tf.keras.layers.Dense(1)
])

print("\nKeras model successfully created!")
model.summary()
