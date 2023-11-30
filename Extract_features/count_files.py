#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:37:14 2023

@author: orane
"""


import parselmouth
from parselmouth.praat import call
import tgt
import glob
import csv
import os

def get_file_lst(path_folder):
    lst_files = glob.glob(path_folder)
    return [f for f in lst_files]

def load_metadata(file):
    lst=[*csv.DictReader(open(file))]     
    return lst

def read_files(file):
    path_wav = file
    path_textgrid = "".join(file.split("/")[:1]) + "/"  + "".join(file.split("/")[1]) + "/" + "".join(file.split("/")[1]) + "_aligned/" + "".join(file.split("/")[2].replace(".wav", ".TextGrid"))
    if os.path.isfile(path_textgrid):
        return True
    else :
        return False
    
metadata = (load_metadata("metadonnees_ESLO2_ENT_ENTJEUN.csv"))
len_folders = len(metadata)
total_phoneme = 0
for i, row in enumerate(metadata) :
            nb_files = 0
            nb_phoneme = 0
            missing_files = 0
            folder = row["directory"]
            print(f"Folder : {folder} ({i + 1}/{len_folders})")
            file_lst = get_file_lst(f"corpus_mfa/{folder}/*.wav")
            for file in file_lst :
                if read_files(file) != False :
                    nb_files += 1
                else :
                    missing_files += 1
            print(f"{missing_files}/{nb_files} fichiers")
            nb_phonemes = nb_files * 3
            total_phoneme += nb_phonemes
            print(f"{nb_phonemes} phones")
            print(f"{total_phoneme} : nombre de phonèmes tous fichier cumulés.")
            

                
