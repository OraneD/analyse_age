#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 23:53:48 2024

@author: orane
"""
import os
import pandas as pd
import numpy as np
import glob
import torch
import librosa
import torchaudio
import numpy as np
import csv
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers import Wav2Vec2Processor
import matplotlib.pyplot as plt
import itertools
from my_minipack.loading import ft_progress

#physical_devices = tf.config.list_physical_devices('GPU')
#tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)
cache_dir = "/mnt/disque_deux/orane"
os.makedirs(cache_dir, exist_ok=True)
model_name = "facebook/wav2vec2-large-xlsr-53-french"
tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = Wav2Vec2ForCTC.from_pretrained(model_name, cache_dir=cache_dir)
processor = Wav2Vec2Processor.from_pretrained(model_name, cache_dir=cache_dir)

def load_metadata(file):
    return [*csv.DictReader(open(file))]  

def get_age_cat(folder, age):
    if "DIA" in folder.split("_") :
        return "old"
    if int(age) < 30 :
        return "young"
    if int(age) > 60 : 
        return "old"
    if int(age) <= 60 and int(age) >= 30 :
        return "mid"

def extract_and_save_vectors(directory):
    print(f"Saving vectors for {directory}")
    print(".....")
    vectors = []
    labels = []
    dico = {"young": 0, "old": 1}
    save_path = os.path.join(directory, "audio_vectors.npz")
    lst_files = glob.glob(directory + "/*.wav")
    for path in lst_files:
        audio_input, sample_rate = torchaudio.load(path)
        if sample_rate != 16000:
            audio_input = torchaudio.functional.resample(audio_input, sample_rate, 16000)

        input_values = processor(audio_input, return_tensors="pt", sampling_rate=16000).input_values
        input_values = input_values.reshape(1, input_values.shape[2])

        with torch.no_grad():
            hidden_state = model(input_values, output_hidden_states=True).hidden_states

        embeddings = hidden_state[0]
        speech_representation = embeddings[0].max(axis=0).values

        x = speech_representation.numpy()
        age = path.split("/")[3]
        y = dico[age]
        vectors.append(x)
        labels.append(y)

    data = np.array(vectors), np.array(labels)
    print(f"{directory} Ok")

    np.savez(save_path, vectors=np.array(vectors), labels=np.array(labels))

    return data

def extract_and_save_vectors_csv(directory, loc, age_cat, sexe,corpus):
    """
    Même chose que la fonction plus haut mais enregistre les vecteurs au format
    csv avec le nom des fichiers et la catégorie en colonne 1 et 2 
    """
    print(f"Saving vectors for {directory}...")
    vectors = []
    labels = []
    filenames = []
    dico = {"young": 0, "old": 1, "mid" : 2}
    save_path =  f"../../Vectors4Sec/{corpus}_vector/{sexe}/{age_cat}/{loc}_0.csv"

    lst_files = glob.glob(f"{directory}*.wav")
    for path in ft_progress(lst_files):
        audio_input, sample_rate = torchaudio.load(path)
        if sample_rate != 16000:
            audio_input = torchaudio.functional.resample(audio_input, sample_rate, 16000)

        input_values = processor(audio_input, return_tensors="pt", sampling_rate=16000).input_values
        input_values = input_values.reshape(1, input_values.shape[2])

        with torch.no_grad():
            hidden_state = model(input_values, output_hidden_states=True).hidden_states

        embeddings = hidden_state[0]
        speech_representation = embeddings[0].max(axis=0).values

        x = speech_representation.numpy()
        y = dico[age_cat]
        filename = os.path.basename(path)

        vectors.append(x)
        labels.append(y)
        filenames.append(filename)

    df = pd.DataFrame(vectors)
    df.insert(0, 'label', labels)
    df.insert(0, 'filename', filenames)
    df.to_csv(save_path, index=False)

    print(f"{directory} Done")
    print()
    return df



#metadata = load_metadata("../../metadonnees_ESLO2_ENT_ENTJEUN.csv")
#for row in metadata:
   # folder = row["directory"]
   # age = row["age"]
   # sexe = row["sexe"]
   # age_cat = get_age_cat(folder, age)
  #  extract_and_save_vectors_csv(folder, age_cat, sexe)
  
#lst_directory = glob.glob("../PTSVOX_4Sec/*/*/*/")
#for file in ft_progress(lst_directory) :
    #sexe = file.split("/")[2]
    #age_cat = file.split("/")[3]
    #loc = file.split("/")[4]
    #if not os.path.exists(f"../../Vectors4Sec/PTSVOX_vector/{sexe}/{age_cat}/{loc}_0.csv"):
       # extract_and_save_vectors_csv(file, loc, age_cat, sexe)
    #else : 
        #continue
        
#lst_directory = glob.glob("../Fabiole1_4Sec/*/*/*/")
#for file in ft_progress(lst_directory) :
    #sexe = file.split("/")[2]
    #age_cat = file.split("/")[3]
    #loc = file.split("/")[4]
    #if not os.path.exists(f"../../Vectors4Sec/Fabiole1_vector/{sexe}/{age_cat}/{loc}_0.csv"):
     #   extract_and_save_vectors_csv(file, loc, age_cat, sexe)
    #else : 
      #  continue
lst_corpus = ["Orfeo", "PFC", "internet"]
for corpus in lst_corpus :    
    lst_directory = glob.glob(f"../{corpus}_4Sec/*/*/*/")
    for file in ft_progress(lst_directory) :
        sexe = file.split("/")[2]
        age_cat = file.split("/")[3]
        loc = file.split("/")[4]
        if not os.path.exists(f"../../Vectors4Sec/{corpus}_vector/{sexe}/{age_cat}/{loc}_0.csv"):
            extract_and_save_vectors_csv(file, loc, age_cat, sexe,corpus)
        else : 
            continue