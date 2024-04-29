from ultralytics import YOLO
import os, time, random
import numpy as np
import pandas as pd
import cv2, torch
from tqdm.auto import tqdm
import shutil as sh
import yaml
import glob
from sklearn.model_selection import train_test_split

from IPython.display import Image, clear_output, display
import matplotlib.pyplot as plt
from IPython import display
display.clear_output()
!yolo mode=checks
%matplotlib inline


import ultralytics
def define_dataset():
    DIR = "distributed_train/datasets/cars/"
    IMAGES = DIR +"images/"
    LABELS = DIR +"labels/"

    TRAIN = "/distributed_train/data/training_images"
    TEST = "distributed_train/data/testing_images"

    df = pd.read_csv("distributed_train/data/train_solution_bounding_boxes (1).csv")
    df.head()

    #setting dataset
    files = list(df.image.unique())

    files_train, files_valid = train_test_split(files, test_size = 0.2)
    return files_train , files_valid


# make directories
def make_dirs(files_train, files_valid):
    os.makedirs(IMAGES+"train", exist_ok=True)
    os.makedirs(LABELS+"train", exist_ok=True)
    os.makedirs(IMAGES+"valid", exist_ok=True)
    os.makedirs(LABELS+"valid", exist_ok=True)


    train_filename = set(files_train)
    valid_filename = set(files_valid)
    for file in glob.glob(TRAIN+"/*"):
        fname =os.path.basename(file)
        if fname in train_filename:
            sh.copy(file, IMAGES+"train")
        elif fname in valid_filename:
            sh.copy(file, IMAGES+"valid")



    for _, row in df.iterrows():    
        image_file = row['image']
        class_id = "0"
        x = row['xmin']
        y = row['ymin']
        width = row['xmax'] - row['xmin']
        height = row['ymax'] - row['ymin']

        x_center = x + (width / 2)
        y_center = y + (height / 2)
        x_center /= 676
        y_center /= 380
        width /= 676
        height /= 380

        if image_file in train_filename:   
            annotation_file = os.path.join(LABELS) + "train/" + image_file.replace('.jpg', '.txt')
        else:
            annotation_file = os.path.join(LABELS) + "valid/" + image_file.replace('.jpg', '.txt')
            
        with open(annotation_file, 'a') as ann_file:
            ann_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
    return 



# Creating yaml file


%%writefile dataset.yaml
# Path
path: ./cars
train: images/train
val: images/valid

# Class
nc: 1
# name of class    
names: ['car']

def train_model();
    #Training the Model from scratch
    model = YOLO()
    model.train(data="/kaggle/working/datasets/cars/dataset.yaml", epochs=50) # train the model

