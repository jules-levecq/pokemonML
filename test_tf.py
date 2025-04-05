import tensorflow as tf

print("Version de TensorFlow :", tf.__version__)
hello = tf.constant("Hello TensorFlow!")
tf.print(hello)
