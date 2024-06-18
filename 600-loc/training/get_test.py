#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:05:21 2024

@author: odufour
"""

import pandas
import glob
import pandas as pd
import numpy as np

def get_ESLO_vector(sexe):
    all_vectors = []
    all_labels = []
    all_filenames = []
    files = glob.glob(f"../Vectors4Sec/ESLO2_vectors_4sec/{sexe}/*/*.csv")
    for file in files :
        df = pd.read_csv(file)
        vectors = df.iloc[:, 2:].to_numpy()
        labels = df['label'].to_numpy()
        filenames = df["filename"].to_list()
        all_vectors.append(vectors)
        all_labels.append(labels)
        all_filenames.extend(filenames)

    X = np.concatenate(all_vectors, axis=0)
    y = np.concatenate(all_labels, axis=0)
    print(f"Final size for test - X : {X.shape}, y : {y.shape}")
    
    return X, y, all_filenames
