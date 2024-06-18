#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 16:35:30 2024

@author: orane
"""

import os
import pandas as pd
import numpy as np
import glob
import torch
import torchaudio
import statistics
import numpy as np
from sklearn.utils import shuffle
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers import Wav2Vec2Processor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import itertools
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.regularizers import l1, l2, l1_l2
from load_vectors import get_basename, load_vectors_csv, load_vectors_csv_files
import csv
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
print(tf.__version__)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
physical_devices = tf.config.list_physical_devices('GPU')
#tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

def scheduler(epoch, lr):
    if epoch < 3:
        return lr
    else:
        return lr * tf.math.exp(-0.01)


model_name = "facebook/wav2vec2-large-xlsr-53-french"
tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)
processor = Wav2Vec2Processor.from_pretrained(model_name)
lst_femme_homme = ["femme", "homme"]

all_accuracy_train = []
all_accuracy_val = []
all_loss_train = []
all_loss_val = []

for sexe in lst_femme_homme:
    accuracy = []
    loc_name = []
    nb_vieux = []
    nb_jeune = []
    nb_test = []
    nb_mid = []
    lst_age = []

    if sexe == "femme":
            checkpoint = ModelCheckpoint('../modeles/best_women_24loc.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
            file_lst = glob.glob("../../Corpus4Sec/ESLO_4Sec/ESLO2_vectors_4sec/femme/*/*.csv")
            for i, file in enumerate(file_lst) : 
                x_test, y_test, test_filenames = load_vectors_csv_files([file])
                test_name = file.split("/")[-1].replace(".csv", "")
                train_lst =  [x for x in file_lst if x != file]
                x_train,y_train, train_filenames = load_vectors_csv_files(train_lst)
                nombre_jeunes = np.sum(y_train == 0)
                nombre_vieux = np.sum(y_train == 1) 
                nombre_mid = np.sum(y_train == 2)
                nb_vieux.append(nombre_vieux)
                nb_jeune.append(nombre_jeunes)
                nb_mid.append(nombre_mid)
                age = file.split("/")[1]
                lst_age.append(age)
                x_train, y_train = shuffle(x_train, y_train)
                
                feature_vector_lenght = 1024
                x_train = x_train.reshape(x_train.shape[0], 1024)
                x_test = x_test.reshape(x_test.shape[0], 1024)
                y_train_1_hot = to_categorical(y_train,num_classes=3)
                y_test_1_hot = to_categorical(y_test, num_classes=3)
                print(f"x_train : {x_train.shape}")
                print(f"x_test : {x_test.shape}")
                test_size = y_test.shape[0]
                nb_test.append(test_size)
                
                model = Sequential()
                #reajust class weight
                class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
                class_weights_dict = dict(enumerate(class_weights))
                feature_vector_length = 1024
                input_shape=(feature_vector_length,)
                model.add(Dense(64, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.01)))
                model.add(Flatten())
                model.add(Dropout(0.2))
                model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
                model.add(Dense(3, activation='softmax'))
                
                
                lr_scheduler = LearningRateScheduler(scheduler)
                early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
                reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.00001)
                #checkpoint = ModelCheckpoint('../modeles/best_men.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
                resume = model.fit(x_train, y_train_1_hot, epochs=50, batch_size=100, verbose=1, validation_data=(x_test,y_test_1_hot),callbacks=[lr_scheduler],class_weight=class_weights_dict)
                history = resume.history
                train_loss = history['loss']
                val_loss = history['val_loss']
                train_accuracy = history.get('accuracy', history.get('acc')) 
                val_accuracy = history.get('val_accuracy', history.get('val_acc'))  
                print(val_accuracy)
                
                
                all_accuracy_train.append(train_accuracy)
                all_accuracy_val.append(val_accuracy)
                all_loss_train.append(train_loss)
                all_loss_val.append(val_loss)
                predictions = model.predict(x_test)
                binary_predictions = np.argmax(predictions, axis=1)
                evaluation = model.evaluate(x_test, y_test_1_hot)
                print(f"Test Accuracy: {evaluation[1] * 100:.2f}%")
                accuracy.append(evaluation[1])
                loc_name.append(test_name)
                predictions = model.predict(x_test)
            
                with open(f"predictions/pred_{test_name}_4sec.csv", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Filename', 'pred_young', "pred_old", "pred_mid"])
                    for path, prediction in zip(test_filenames, predictions):
                        young_pred = prediction[0]
                        old_pred = prediction[1]
                        mid_pred = prediction[2]
                        writer.writerow([path, young_pred, old_pred, mid_pred])
                reponses = np.array(y_test)
                predictions = np.argmax(predictions, axis = 1)
                print(classification_report(y_test, predictions))
           # with open('accuracy_femmes_4sec.csv', 'w', newline='') as f:
            #    writer = csv.DictWriter(f, fieldnames=["locuteurs", "age", "accuracy", "jeune_train", "vieux_train", "mid_train" ,"test"])
             #   writer.writeheader()
            
              #  for i in range(len(accuracy)):
               #     row_dict = {
                #        "locuteurs": loc_name[i],
                 #       "age" : lst_age[i],
                  #      "accuracy": accuracy[i],
                   #     "jeune_train": nb_jeune[i],
                    #    "vieux_train": nb_vieux[i],
                     #   "mid_train"  : nb_mid[i],
                      #  "test": nb_test[i]  
                    #}
                   # writer.writerow(row_dict)
        
    elif sexe == "homme":
            checkpoint = ModelCheckpoint('../modeles/best_men_24loc.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
            file_lst = glob.glob("../../Corpus4Sec/ESLO_4Sec/ESLO2_vectors_4sec/homme/*/*.csv")
            for i, file in enumerate(file_lst) : 
                x_test, y_test, test_filenames = load_vectors_csv_files([file])
                test_name = file.split("/")[-1].replace(".csv", "")
                train_lst =  [x for x in file_lst if x != file]
                x_train,y_train, train_filenames = load_vectors_csv_files(train_lst)
                nombre_jeunes = np.sum(y_train == 0)
                nombre_vieux = np.sum(y_train == 1) 
                nombre_mid = np.sum(y_train == 2)
                nb_vieux.append(nombre_vieux)
                nb_jeune.append(nombre_jeunes)
                nb_mid.append(nombre_mid)
                age = file.split("/")[1]
                lst_age.append(age)
                x_train, y_train = shuffle(x_train, y_train)
                
                feature_vector_lenght = 1024
                class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
                class_weights_dict = dict(enumerate(class_weights))
                x_train = x_train.reshape(x_train.shape[0], 1024)
                x_test = x_test.reshape(x_test.shape[0], 1024)
                y_train_1_hot = to_categorical(y_train,num_classes=3)
                y_test_1_hot = to_categorical(y_test, num_classes=3)
                print(f"x_train : {x_train.shape}")
                print(f"x_test : {x_test.shape}")
                test_size = y_test.shape[0]
                nb_test.append(test_size)
                
                model = Sequential()
                feature_vector_length = 1024
                input_shape=(feature_vector_length,)
                model.add(Dense(64, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.01)))
                model.add(Flatten())
                model.add(Dropout(0.2))
                model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
                model.add(Dense(3, activation='softmax'))
                
                
                lr_scheduler = LearningRateScheduler(scheduler)
                early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
                reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.00001)
                #checkpoint = ModelCheckpoint('../modeles/best_men.h5', monitor='val_accuracy',verbose=1,save_best_only=True, mode='max' )
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
                resume = model.fit(x_train, y_train_1_hot, epochs=50, batch_size=100, verbose=1, validation_data=(x_test,y_test_1_hot),callbacks=[lr_scheduler],class_weight=class_weights_dict)
                history = resume.history
                train_loss = history['loss']
                val_loss = history['val_loss']
                train_accuracy = history.get('accuracy', history.get('acc')) 
                val_accuracy = history.get('val_accuracy', history.get('val_acc'))  
                
                
                all_accuracy_train.append(train_accuracy)
                all_accuracy_val.append(val_accuracy)
                all_loss_train.append(train_loss)
                all_loss_val.append(val_loss)
                predictions = model.predict(x_test)
                binary_predictions = np.argmax(predictions, axis=1)
                evaluation = model.evaluate(x_test, y_test_1_hot)
                print(f"Test Accuracy: {evaluation[1] * 100:.2f}%")
                accuracy.append(evaluation[1])
                loc_name.append(test_name)
                predictions = model.predict(x_test)
            
                with open(f"predictions/pred_{test_name}_4sec.csv", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Filename', 'pred_young', "pred_old", "pred_mid"])
                    for path, prediction in zip(test_filenames, predictions):
                        young_pred = prediction[0]
                        old_pred = prediction[1]
                        mid_pred = prediction[2]
                        writer.writerow([path, young_pred, old_pred, mid_pred])
                reponses = np.array(y_test)
                predictions = np.argmax(predictions, axis = 1)
                print(classification_report(y_test, predictions))
           # with open('accuracy_homme_4sec.csv', 'w', newline='') as f:
               # writer = csv.DictWriter(f, fieldnames=["locuteurs", "age", "accuracy", "jeune_train", "vieux_train", "mid_train", "test"])
               # writer.writeheader()
            
              #  for i in range(len(accuracy)):
                 #   row_dict = {
                    #    "locuteurs": loc_name[i],
                     #  "age" : lst_age[i],
                       # "accuracy": accuracy[i],
                       # "jeune_train": nb_jeune[i],
                       # "vieux_train": nb_vieux[i],
                       # "mid_train"  : nb_mid[i],
                        #"test": nb_test[i]  
                    #}
                   # writer.writerow(row_dict)

mean_val_accuracy = [sum(group) / len(group) for group in list(zip(*all_accuracy_val))]
mean_train_accuracy = [sum(group) / len(group) for group in list(zip(*all_accuracy_train))]
mean_val_loss = [sum(group) / len(group) for group in list(zip(*all_loss_val))]
mean_train_loss = [sum(group) / len(group) for group in list(zip(*all_loss_train))]

assert len(mean_train_loss) == 50, "mean_train_loss n'a pas 50 points"
assert len(mean_val_loss) == 50, "mean_val_loss n'a pas 50 points"
assert len(mean_train_accuracy) == 50, "mean_train_accuracy n'a pas 50 points"
assert len(mean_val_accuracy) == 50, "mean_val_accuracy n'a pas 50 points"   
     
plt.figure(figsize=(16, 7))
plt.subplot(1, 2, 1)
plt.plot(mean_train_loss, label='Entraînement Loss', color = "tab:green")
plt.plot(mean_val_loss, label='Validation Loss', color = "black", linestyle = "--")
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(mean_train_accuracy, label='Entraînement Précision',  color = "tab:green")
plt.plot(mean_val_accuracy, label='Validation Précision', color = "black", linestyle = "--")
plt.title('Précision')
plt.xlabel('Epochs')
plt.ylabel('Précision')
plt.legend()
plt.grid()

plt.show()