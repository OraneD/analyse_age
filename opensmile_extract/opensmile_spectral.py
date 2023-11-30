#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 02:21:36 2023

@author: orane
"""

import opensmile
import os
import glob
import csv
import tgt
import soundfile as sf
import pandas as pd


def get_time_sound(sound):
    f = sf.SoundFile(sound)
    return len(f) / f.samplerate

def get_file_lst(path_folder):
    return glob.glob(path_folder)


def load_metadata(file):
    return [*csv.DictReader(open(file))] 


def extract_interval_tier(textgrid):
    return textgrid.get_tier_by_name("phones")    


def get_spectral_features(file_sound, tier):
    smile = opensmile.Smile(
            feature_set="IS12_speaker_trait.conf",
            feature_level="spectral",
            loglevel=2,
            logfile='smile.log',)
    spectral_df = smile.process_file(file_sound)
    phon = []
    for i in range(0,len(spectral_df.index)) :
       start_time = i / 100
       intervals = tier.get_annotations_by_time(start_time)
       if intervals == [] :
           label = "_" 
       for interval in intervals :
           label = interval.text
       phon.append(label)

    return phon, spectral_df

def read_files(file):
    path_wav = file
    path_textgrid =  "../../corpus_mfa/"  + "".join(file.split("/")[3]) + "/" + "".join(file.split("/")[3]) + "_aligned/" + "".join(file.split("/")[4].replace(".wav", ".TextGrid"))
    if os.path.isfile(path_textgrid):
        textgrid = tgt.io.read_textgrid(path_textgrid)
        return textgrid
    else :
        return False

def main():
    metadata = (load_metadata("../../small_corpus_metadata.csv"))
    corpus_features = pd.DataFrame()
    for i, row in enumerate(metadata) :
            missing_file = 0
            total_phon = []
            total_features = pd.DataFrame()
            folder = row["directory"]
            age = row["age"]
            sexe = row["sexe"]
            categorie_pro = row["categorie_professionnelle"]
            niveau_etude = row["niveau_etude"]
            print(f"Folder : {folder}")
            file_lst = get_file_lst(f"../../Corpus_mfa/{folder}/*.wav")
            for file in file_lst :
                if read_files(file) :
                    textgrid = read_files(file)
                    tier = extract_interval_tier(textgrid)
                    phonemes,features = get_spectral_features(file,tier)
                    total_phon.extend(phonemes)
                    total_features = pd.concat([total_features,features])
                    if len(total_features.index) != len(total_phon) :
                        break
                else :
                    missing_file += 1
                    continue
            total_features["phonemes"]= total_phon
            total_features["age"] = [age]*len(total_phon)
            total_features["sexe"] = [sexe]*len(total_phon)
            total_features["categorie_professionnelle"] = [categorie_pro]*len(total_phon)
            total_features["niveau_etude"] = [niveau_etude]*len(total_phon)
            print(f"Completed : {missing_file}/{len(file_lst)} missing files ")
            print(total_features.head())
            corpus_features = pd.concat([corpus_features,total_features])
            
    corpus_features.to_csv("test_resultats.csv")
    print("End of processing ")

    

if __name__ == "__main__" :
    main()