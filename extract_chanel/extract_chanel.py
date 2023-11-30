#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 15:35:36 2023

@author: orane
"""
import glob
import csv
import os
import parselmouth
from parselmouth.praat import call
import tgt


def get_file_lst(path_folder):
    return glob.glob( path_folder)

def load_metadata(file):
    return [*csv.DictReader(open(file))]   

def read_files(file):
    path_wav =  file
    sound = parselmouth.Sound(path_wav)
    return sound

      
def extract_one_channel(sound_object):
    if call(sound_object, "Get number of channels") > 1 :
        left = call(sound_object, "Extract one channel", "Left")
        right = call(sound_object, "Extract one channel", "Right")
        intensity_left = call(left, "Get intensity (dB)")
        intensity_right = call(right, "Get intensity (dB)")
        
        if intensity_left > intensity_right :
            print("Left channel selected (1)")
            return left
        else :
            print("Right channel selected (2)")
            return right
    else :
        return "One Channel File"
    


def main() :
    metadata = (load_metadata("../modules_ESLO/module_diachronie/metadonnees_diachronie.csv"))
    len_folders = len(metadata)

    for i, row in enumerate(metadata) :
        folder = row["directory"]
        print(f"Folder : {folder} ({i + 1}/{len_folders})")
        sound = read_files(f"../modules_ESLO/module_diachronie/diachronie_1_tier/{folder}/{folder}_T1.wav")
        channel = extract_one_channel(sound)
        if channel != "One Channel File" :
            channel.save(f"../modules_ESLO/module_diachronie/diachronie_1_tier/{folder}/{folder}_T1.wav", "WAV")
        else :
            print(f"{folder} has only one channel")
        print("Extraction Completed")

main()
        
            
            
    
    
    