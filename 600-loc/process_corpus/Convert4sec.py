#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:04:00 2024

@author: orane
"""


import parselmouth
from parselmouth.praat import call
import tgt
import glob
import csv
import os

def get_file_lst(path_folder):
    return glob.glob("../../corpus_mfa_1channel/" + path_folder)

def load_metadata(file):
    return [*csv.DictReader(open(file))]     

def extract_interval_tier(textgrid):
    return textgrid.get_tier_by_name("phones")

def get_basename(file):
    return file.split("/")[-1].replace(".wav", "")


def read_files(file):
    basename = get_basename(file)
    folder = "_".join(basename.split("_")[:3])
    path_wav =  file
    path_textgrid = "/".join(path_wav.split("/")[:4]) + f"/{folder}_aligned/" + basename + ".TextGrid"

    if os.path.isfile(path_textgrid):
        sound = parselmouth.Sound(path_wav)
        textgrid = tgt.io.read_textgrid(path_textgrid)
        return sound, textgrid
    else :
        return False
    
def main():
    file_lst = get_file_lst("ESLO2_ENT_1001/*.wav")
    duration_extract = 0
    sound_to_copy = parselmouth.Sound("../../corpus_mfa_1channel/ESLO2_ENT_1001/ESLO2_ENT_1001_T1_3.wav")
    new_sound = sound_to_copy.extract_part(0, 0.01, parselmouth.WindowShape.RECTANGULAR, 1, False)
    i = 0
    num_sound = 0
    while i < len(file_lst) :
        if not read_files(file_lst[i]) :
            i += 1
            continue
        sound,textgrid = read_files(file_lst[i])
        duration_current =  call(sound,"Get total duration")
        print(i)
        if duration_extract < 4 :
            print(f"Duree Inférieure {duration_extract}")
            duration_extract += duration_current
            if duration_extract < 4 :
                new_sound = new_sound.concatenate([sound])
            elif duration_extract > 4 :
                end_time = sound.get_end_time()
                surplus = duration_extract - 4
                extract_sound = sound.extract_part(0,surplus, parselmouth.WindowShape.RECTANGULAR, 1,False,)
                new_sound = new_sound.concatenate([extract_sound])
                new_sound = sound.extract_part(surplus,end_time, parselmouth.WindowShape.RECTANGULAR, 1,False,)
                if duration_extract == 4 :
                    print(f"Durée Bonne {duration_extract}")
                    new_sound.save(f"../ESLO2_ENT_1001/ESLO2_ENT_1001_{num_sound}.wav", "WAV")
                    duration_extract = 0
                    num_sound += 1
            i += 1
            continue
        if duration_extract > 4 :
            print(f"Duree Supérieure {duration_extract}")
            surplus = duration_extract - 4 
            duration_extract -= surplus
            i += 1
            continue
        if duration_extract == 4 :
            print(f"Durée Bonne {duration_extract}")
            new_sound.save(f"../ESLO2_ENT_1001/ESLO2_ENT_1001_{num_sound}.wav", "WAV")
            duration_extract = 0
            num_sound += 1
            continue

                
                
            


    
main()