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

def create_datasets():
    DIR = "/home/hungnguyen/Capstone-Project-Model-Serving/distributed_trainning/data/"
    IMAGES = DIR +"images/"
    LABELS = DIR +"labels/"   

    TRAIN = "/home/hungnguyen/Capstone-Project-Model-Serving/distributed_trainning/data/training_images"
    TEST = "/home/hungnguyen/Capstone-Project-Model-Serving/distributed_trainning/data/testing_images"

    df = pd.read_csv("/home/hungnguyen/Capstone-Project-Model-Serving/distributed_trainning/data/train_solution_bounding_boxes (1).csv")
    files = list(df.image.unique())

    files_train, files_valid = train_test_split(files, test_size = 0.2)

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

    

if __name__ == "__main__":
    create_datasets()
    