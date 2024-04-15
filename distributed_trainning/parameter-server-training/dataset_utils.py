import numpy as np
import tensorflow as tf


# Scale MNIST data from (0, 255] to (0., 1.]
def scale(image):
    image = image.astype(np.float32)
    image /= 255
    return image


def create_datasets(buffer_size, batch_size):
    # Load the dataset MNIST from TensorFlow in a supervised format
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # Scale the datasets and make batches. For train_dataset,
    # we also want to shuffle it with a predefined buffer size
    x_train = scale(x_train)
    x_test = scale(x_test)

    # Scale the the training data, cache it to the main memory
    # then shuffle with the
    train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test))

    train_dataset = train_dataset.cache().shuffle(buffer_size).batch(batch_size)
    test_dataset = test_dataset.batch(batch_size)

    return train_dataset, test_dataset
