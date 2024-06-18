#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:30:09 2024

@author: odufour
"""
import pandas as pd
import csv
import glob
import numpy as np

def load_metadata():
    df = pd.read_csv("train_corpus_time.csv")
    df.to_csv("train_corpus_time_test.csv")
    return pd.read_csv("train_corpus_time.csv")

def get_metadata_per_sexe(metadata, sexe):
    df_sexe = metadata[metadata["sexe"] == sexe]
    df_2min = df_sexe[df_sexe["sup2min"] == True]
    return df_2min

def get_corpus_name(corpus):
    if corpus == "orfeo":
        return "Orfeo_vector"
    elif corpus == "PFC" or corpus == "pfc" :
        return "PFC_vector"
    elif corpus == "corpus_internet":
        return "internet_vector"
    elif corpus == "fabiole_2":
        return "Fabiole2_vector"
    elif corpus == "fabiole_1":
        return "Fabiole1_vector"
    elif corpus == "PTSVOX" :
        return "PTSVOX_vector"
    elif corpus == "commonvoice":
        return "commonvoice_vector"

def get_vector(file_path):
    df = pd.read_csv(file_path)
    vectors = df.iloc[:, 2:].to_numpy()[:31]
    labels = df['label'].to_numpy()[:31]
    filenames = df["filename"].to_list()[:31]
    #if len(vectors) != 31 :
        #print(file_path, vectors.shape)
    return vectors, labels, filenames

def mix_loc(metadata):
    if len(metadata) > 100:
        return metadata.sample(n=100, random_state=42)
    return metadata
    
def get_all_vector_1cat(metadata, age_cat):
    all_vectors = []
    all_labels = []
    all_filenames = []
    df_age_cat = metadata[metadata["age_cat"] == age_cat]
    df_age_cat = mix_loc(df_age_cat)
    for row in df_age_cat.itertuples() :
        corpus = get_corpus_name(row.corpus)
        loc = row.loc
        sexe = row.sexe
        file_path = glob.glob(f"../Vectors4Sec/{corpus}/{sexe}/{age_cat}/*{loc}*.csv")[0]
        vectors, labels, filenames = get_vector(file_path)
        all_vectors.append(vectors)
        all_labels.append(labels)
        all_filenames.extend(filenames)

    X = np.concatenate(all_vectors, axis=0)
    y = np.concatenate(all_labels, axis=0)
    return X, y, all_filenames

def get_full_corpus_vector(metadata):
    all_filenames = []
    print("Charging vectors for mid......")
    X_mid, y_mid, filenames_mid = get_all_vector_1cat(metadata, "mid")
    print(f"Vector for mid charged : {len(X_mid)}")
    print()
    print("Charging vectors for old......")
    X_old, y_old, filenames_old = get_all_vector_1cat(metadata, "old")
    print(f"Vector for old charged : {len(X_old)}")
    print()
    print("Charging vectors for young......")
    X_young, y_young, filenames_young = get_all_vector_1cat(metadata, "young")
    print(f"Vector for young charged : {len(X_young)}")
    X = np.concatenate([X_mid, X_old, X_young], axis=0)
    y = np.concatenate([y_mid, y_old, y_young], axis = 0)
    all_filenames.extend(filenames_mid)
    all_filenames.extend(filenames_old)
    all_filenames.extend(filenames_young)
    return X, y, all_filenames


    
    
    

    
    