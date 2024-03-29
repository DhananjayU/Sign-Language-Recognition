# -*- coding: utf-8 -*-
"""LargeDatasetModel(Modified Alexnet).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZNgtkCL_IYB60SotMcVgWlD63JvZ7StG
"""
#clone the dataset into a folder before running this 
#!git clone https://github.com/DhananjayU/dataset

from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras import layers
import numpy as np
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D,Dense,BatchNormalization,Dropout
from tensorflow.keras.layers import Flatten
from keras.regularizers import l2
from keras.datasets import cifar10
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator

from keras.utils.np_utils import to_categorical

import os
import cv2
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-bp", "--base_path", 
	help="The base path of the directory", 
	default="./Dataset1/train/")

parser.add_argument("-v", "--val_split", type=float, help="Validation split", default=0.2)  
parser.add_argument("-b", "--batch_size", type=int, help="Batch size", default=8)
parser.add_argument("-k", "--k_fold", type=int, help="Value of k for k-fold validation", default=5)
parser.add_argument("-e", "--epochs", type=int, help="Number of epochs", default=1)
parser.add_argument("-d", "--dropout", type=float, help="Dropout probability for dense layers", default=0.5)
parser.add_argument("-l", "--learning_rate", type=float, help="Learning rate", default=.001)

args = parser.parse_args()

base=args.base_path
b_size=args.batch_size
kf=args.k_fold
eps=args.epochs
drop=args.dropout
lrate=args.learning_rate
vsplit=args.val_split

print(args)

model = Sequential()
model.add(Conv2D(32, kernel_size = (5, 5), activation='relu',kernel_regularizer=l2(0.001), input_shape=(224,224,1)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=(5,5), kernel_regularizer=l2(0.001),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=(5,5), kernel_regularizer=l2(0.001),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(96, kernel_size=(5,5), kernel_regularizer=l2(0.001),activation='relu'))  
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Conv2D(32, kernel_size=(5,5), kernel_regularizer=l2(0.001),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization())
model.add(Dropout(drop))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(drop))
model.add(Dense(26, activation = 'softmax'))

print("Model Created")

cvscores = []
data_path=base

# os.chdir("dataset/asl_alphabet_train/asl_alphabet_train/")
# k fold validation

print("Model training and k-fold validation starting for k="+kf)
for k in range(kf):
  train_datagen = ImageDataGenerator(validation_split = 0.2)

  train_generator = train_datagen.flow_from_directory(data_path,
                                                    target_size = (224,224),
                                                    color_mode = 'grayscale',
                                                    batch_size = b,
                                                    class_mode = 'sparse',
                                                    shuffle = True,
                                                    subset = 'training')
  validation_generator = train_datagen.flow_from_directory(data_path,
                                                    target_size = (224,224),
                                                    color_mode = 'grayscale',
                                                    batch_size = b,
                                                    class_mode = 'sparse',
                                                    shuffle = True,
                                                    subset = 'validation')
  model.compile(loss='sparse_categorical_crossentropy',optimizer = 'Adam', metrics=['accuracy'])
  
  step_size_train = train_generator.n//train_generator.batch_size
  
  model.fit_generator(generator = train_generator, steps_per_epoch = step_size_train, epochs=eps, verbose=1)
  
  scores = model.evaluate_generator(generator = validation_generator,verbose=1)
  
  print("%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))
  
  cvscores.append(scores[1]*100)
  
print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores),np.std(cvscores)))

print("%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))
  
cvscores.append(scores[1]*100)

print("Starting loading test data and testing")

images=[]
labels=[]

for i in os.listdir(data_path+"../test"):
  img=cv2.imread(i,0)
  images.append(cv2.resize(img,(224,224)))
  labels.append(ord(i[0])-65)

images=np.array(images)
labels=np.array(labels)

print(images.shape)
print(labels.shape)

scores=model.evaluate(x=images.reshape(images.shape[0],224,224,1),y=labels)

print("%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))