#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:48:31 2024

@author: orane
"""

import opensmile
import os
import glob
import csv
import tgt
import soundfile as sf
import pandas as pd
from datetime import timedelta
import sys
from my_minipack.loading import ft_progress


def get_age_cat(age):
    if age == "vieux":
        return "old"
    elif int(age) < 30 :
        return "young"
    elif int(age) >= 30 and int(age) <= 60 :
        return "mid"
    elif int(age) > 60 :
        return "old"

def get_time_sound(sound):
    f = sf.SoundFile(sound)
    return len(f) / f.samplerate

def get_file_lst(path_folder):
    return glob.glob(path_folder)


def load_metadata(file):
    return [*csv.DictReader(open(file))] 


def get_spectral_features(file_sound, conf_file):
    smile = opensmile.Smile(
            feature_set= conf_file,
            feature_level="spectral",
            loglevel=2,
            logfile='smile.log',)
    spectral_df = smile.process_file(file_sound)
    return spectral_df

def matrix_to_singlevector(df):
    new_dataframe = pd.DataFrame()
    opensmile_features = [
       'pcm_fftMag_fband250-650', 'pcm_fftMag_fband1000-4000',
       'pcm_fftMag_spectralRollOff25.0', 'pcm_fftMag_spectralRollOff50.0',
       'pcm_fftMag_spectralRollOff75.0', 'pcm_fftMag_spectralRollOff90.0',
       'pcm_fftMag_spectralFlux', 'pcm_fftMag_spectralCentroid',
       'pcm_fftMag_spectralEntropy', 'pcm_fftMag_spectralVariance',
       'pcm_fftMag_spectralSkewness', 'pcm_fftMag_spectralKurtosis',
       'pcm_fftMag_spectralSlope', 'pcm_fftMag_psySharpness',
       'pcm_fftMag_spectralHarmonicity'
    ]
    columns_to_concat = []
    for feature in opensmile_features:
           if feature in df.columns:
               for i in range(len(df)):
                   new_col_name = f"{feature}-{i}"
                   # Create a Series for each new column
                   new_series = pd.Series(df[feature].iloc[i], name=new_col_name)
                   columns_to_concat.append(new_series)
   
       # Concatenate all Series to form the new dataframe
    new_dataframe = pd.concat(columns_to_concat, axis=1)
    return new_dataframe
        


def main():
    if len(sys.argv) != 2:
        sys.exit("Entrez le nom du fichier de config en argument.")
    conf_file = sys.argv[1]
    metadata = (load_metadata("../../metadonnees_ESLO2_ENT_ENTJEUN.csv"))
    with open("folder_processed.txt", "r") as processed :
        folder_processed = [x.strip() for x in processed.readlines()]
    for i, row in enumerate(metadata) :
            missing_file = 0
            folder = row["directory"]
            age = get_age_cat(row["age"])
            sexe = row["sexe"]
            if folder in folder_processed :
                print(f"{folder} already processed")
                continue
            with open("folder_processed.txt", "a") as processed :
                processed.write(f"{folder} \n")
            if not os.path.exists(f"IS12_SingleVector_4sec_concat/{sexe}/{age}/{folder}/"):
                os.mkdir(f"IS12_SingleVector_4sec_concat/{sexe}/{age}/{folder}/")
            print(f"Folder : {folder}")
            file_lst = get_file_lst(f"../../Corpus4Sec/ESLO_4Sec/{folder}/*.wav")
            for file in ft_progress(file_lst) :
                    if get_time_sound(file) == 4 :
                        filename = file.split("/")[-1].replace(".wav", "")
                        spectral_df = get_spectral_features(file, conf_file)
                        spectral_df_concat = matrix_to_singlevector(spectral_df)
                        spectral_df_concat.to_csv(f"IS12_SingleVector_4sec_concat/{sexe}/{age}/{folder}/{filename}_IS12_1vec_concat.csv")
            print(f"Folder {folder} processed")
            



    print("End of processing ")
    
main()