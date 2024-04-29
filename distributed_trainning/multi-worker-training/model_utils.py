import tensorflow as tf
from tensorflow.keras import layers, models
from ultralytics import YOLO

def build_model():
    model = YOLO(data="./dataset.yaml", epochs=10)
    return model
