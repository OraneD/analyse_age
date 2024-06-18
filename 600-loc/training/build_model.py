#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:34:32 2024

@author: odufour
"""
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.regularizers import l1, l2, l1_l2
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.utils import class_weight
from get_train import get_metadata_per_sexe, load_metadata, get_full_corpus_vector
from get_test import get_ESLO_vector
import matplotlib.pyplot as plt


def load_train(metadata, sexe):
    metadata_split = get_metadata_per_sexe(metadata, sexe)
    X_train, y_train, all_filenames_train = get_full_corpus_vector(metadata_split)
    print(f"Final size for train - X : {X_train.shape}, y : {y_train.shape}")
    return X_train, y_train, all_filenames_train
    
metadata = load_metadata()
X_train, y_train, all_filenames_train = load_train(metadata, "femme")
x_test, y_test, all_filenames_test = get_ESLO_vector("femme")
y_train_1_hot = to_categorical(y_train,num_classes=3)
y_test_1_hot = to_categorical(y_test, num_classes=3)
y_train_classes = np.argmax(y_train_1_hot, axis=1)

class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_train_classes), y=y_train_classes)
class_weights_dict = dict(enumerate(class_weights))


model = Sequential()
feature_vector_length = 1024
input_shape=(feature_vector_length,)
model.add(Dense(32, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.1)))
model.add(BatchNormalization())  
model.add(Dense(32, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.1)))
model.add(BatchNormalization())  
model.add(Dense(32, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.1)))
model.add(BatchNormalization())  
model.add(Dropout(0.3))
model.add(Dense(32, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.1)))
model.add(BatchNormalization())  
model.add(Dense(32, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.1)))
model.add(BatchNormalization())  
model.add(Dropout(0.5))

model.add(Dense(32, input_shape=input_shape, activation='relu',kernel_regularizer=l2(0.1)))
model.add(BatchNormalization())  
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dense(16, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dense(3, activation='softmax'))


early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.00001)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
resume = model.fit(X_train, y_train_1_hot, epochs=100, batch_size=200, verbose=1, validation_data=(x_test,y_test_1_hot),callbacks=[reduce_lr], class_weight=class_weights_dict)

predictions = model.predict(x_test)
binary_predictions = np.argmax(predictions, axis=1)
evaluation = model.evaluate(x_test, y_test_1_hot)
print(f"Test Accuracy: {evaluation[1] * 100:.2f}%")
predictions = model.predict(x_test)

y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test_1_hot, axis=1)
cm = confusion_matrix(y_test_classes, y_pred_classes)
class_names = ['Jeune', 'Vieux', 'Milieu']
def print_confusion_matrix(confusion_matrix, class_names):
    print('Matrice de Confusion\n')
    print("                      Prediction")
    print()
    row_format ="{:>10}" * (len(class_names) + 1)
    print(row_format.format("", *class_names))
    for name, row in zip(class_names, confusion_matrix):
        print(row_format.format(name, *row))
print_confusion_matrix(cm, class_names)


print("\nClassification Report:")
print()
report = classification_report(y_test_classes, y_pred_classes, target_names=['Jeune', 'Vieux', 'Milieu'])
print(report)

plt.figure(figsize=(16, 7))
plt.subplot(1, 2, 1)
plt.plot(resume.history['loss'], label='Entraînement Loss', color="tab:green")
plt.plot(resume.history['val_loss'], label='Validation Loss', color="black", linestyle="--")
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid()
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(resume.history['accuracy'], label='Entraînement Précision', color="tab:green")
plt.plot(resume.history['val_accuracy'], label='Validation Précision',color="black", linestyle="--")
plt.title('Précision')
plt.xlabel('Epochs')
plt.ylabel('Précision')
plt.grid()
plt.legend()

plt.show()
