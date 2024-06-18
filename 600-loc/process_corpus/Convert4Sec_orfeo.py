#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:32:51 2024

@author: odufour
"""

import csv
import parselmouth
from parselmouth.praat import call
import glob
import csv
import os
from my_minipack.loading import ft_progress

def load_metadata(file):
    return [*csv.DictReader(open(file))]

def get_age_cat(age):
    if age == "Inconnu" or age == "":
        return False
    if int(age) < 30 :
        return "young"
    if int(age) >= 30 and int(age) <= 60 :
        return "mid"
    if int(age) > 60 :
        return "old"



def read_files(file):
        return parselmouth.Sound(file)


def concatenate_corpus(path):
    file_lst = glob.glob(path)
    temp = parselmouth.Sound(file_lst[0])
    new_sound = temp.extract_part(
        0, 0.01, parselmouth.WindowShape.RECTANGULAR, 1, False
    )
    print("Concatenating sounds...")
    for file in ft_progress(file_lst):
        sound = read_files(file)
        if call(sound, "Get total duration") > 180 :
            continue
        new_sound = new_sound.concatenate([new_sound,sound])
    duration = call(new_sound,"Get total duration")
    print(f"Folder concatenated : duration : {duration}")
    return new_sound
        
def cut_every4sec(full_sound,loc, age_cat , sexe):
    duration_sound = call(full_sound, "Get total duration")
    start = 0
    end = 4
    num_file = 0
    print("Cutting Sound.....")
    while start <= duration_sound :
        sound_4sec = full_sound.extract_part(start, end, parselmouth.WindowShape.RECTANGULAR, 1, False)
        sound_4sec.save(f"../Orfeo_4Sec/{sexe}/{age_cat}/{loc}/{loc}_4Sec_{num_file}.wav", "WAV")
        num_file += 1
        start += 4
        end += 4
            
def main():
    folder_lst = glob.glob("../../corpus_orfeo/*/*/*")
    for folder in ft_progress(folder_lst):
        loc = folder.split("/")[-1]
        age_cat = folder.split("/")[-2]
        sexe = folder.split("/")[-3]
        if not os.path.exists(f"../Orfeo_4Sec/{sexe}/{age_cat}/{loc}"):
            os.mkdir(f"../Orfeo_4Sec/{sexe}/{age_cat}/{loc}")
            path = f"{folder}/*.wav"
            full_sound = concatenate_corpus(path)
            cut_every4sec(full_sound,loc,age_cat,sexe)

    
if __name__ == "__main__" :
    main()
