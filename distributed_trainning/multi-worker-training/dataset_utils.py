import tensorflow as tf
import tensorflow_datasets as tfds


# Scale MNIST data from (0, 255] to (0., 1.]
def scale(image, label):
    image = tf.cast(image, tf.float32)
    image /= 255
    return image, label


def create_datasets(buffer_size, batch_size):
    # Load the dataset MNIST from TensorFlow in a supervised format
    datasets, _ = tfds.load(name="cars196", with_info=True, as_supervised=True)
    mnist_train, mnist_test = datasets["train"], datasets["test"]

    # Scale the datasets and make batches. For train_dataset,
    # we also want to shuffle it with a predefined buffer size
    train_dataset = (
        mnist_train.map(scale).cache().shuffle(buffer_size).batch(batch_size)
    )
    eval_dataset = mnist_test.map(scale).batch(batch_size)

    # Scale the the training data, cache it to the main memory
    # then shuffle with the
    return train_dataset, eval_dataset
