from abc import ABC, abstractmethod

import tensorflow as tf
from tensorflow.keras.layers import Dense, InputLayer
from sklearn.metrics import confusion_matrix, f1_score

from alibi_detect.od import IForest, OutlierVAE
from alibi_detect.saving import save_detector, load_detector

# Define some constants
SUPPORTED_MODELS = ["vae", "isf"]


def initialize_vae(n_features, latent_dim):
    """
    Make an vae model
    """
    encoder_net = tf.keras.Sequential(
        [
            InputLayer(input_shape=(n_features,)),
            Dense(20, activation=tf.nn.relu),
            Dense(15, activation=tf.nn.relu),
            Dense(7, activation=tf.nn.relu),
        ]
    )

    decoder_net = tf.keras.Sequential(
        [
            InputLayer(input_shape=(latent_dim,)),
            Dense(7, activation=tf.nn.relu),
            Dense(15, activation=tf.nn.relu),
            Dense(20, activation=tf.nn.relu),
            Dense(n_features, activation=None),
        ]
    )

    # initialize outlier detector
    vae = OutlierVAE(
        threshold=None,  # threshold for outlier score
        score_type="mse",  # use MSE of reconstruction error for outlier detection
        encoder_net=encoder_net,  # can also pass VAE model instead
        decoder_net=decoder_net,  # of separate encoder and decoder
        latent_dim=latent_dim,
        samples=5,
    )

    return vae


class Trainer(object):
    """
    Base class for all trainers
    """

    def __init__(self, model_name="vae", *args, **kwargs):
        self.model_name = model_name.lower()
        if model_name in SUPPORTED_MODELS:
            self.model = initialize_vae(*args, **kwargs)
        else:
            raise ValueError(f"Unsupported model {model_name} for Trainer!")

    def train(self, X_train, perc_outlier, *args, **kwargs):
        self.model.fit(X_train, *args, **kwargs)

        # Infer outlier threshold
        self.model.infer_threshold(X_train, threshold_perc=100 - perc_outlier)

    def load_model(self, filepath):
        self.model = load_detector(filepath)

    def predict(self, X_test, *args, **kwargs):
        return self.model.predict(X_test, *args, **kwargs)

    @staticmethod
    def evaluate(y_test, y_pred):
        score = f1_score(y_test, y_pred)
        return score

    def save_model(self, filepath):
        save_detector(self.model, filepath)

