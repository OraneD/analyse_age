#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 00:28:31 2024

@author: orane
"""

import parselmouth
from parselmouth.praat import call
import tgt
import glob
import csv
import os


TARGET_DUR = 4

def adjust_duration_to_target(current_sound, num_sound,loc, file_name, age, sexe):
    duration_time = call(current_sound, "Get total duration")
    if duration_time < TARGET_DUR:
        print(f"error at extract {num_sound}")
    right_part = current_sound.extract_part(
        0, TARGET_DUR, parselmouth.WindowShape.RECTANGULAR, 1, False
    )
    right_part.save(f"../Corpus4Sec/PTSVOX_4Sec/{sexe}/{age}/{loc}/{file_name}_{num_sound}.wav", "WAV")
    return current_sound.extract_part(
        TARGET_DUR, duration_time, parselmouth.WindowShape.RECTANGULAR, 1, False
    )

def read_files(file):
        return parselmouth.Sound(file)

def add_files_until_target(new_sound, current_sound, file_lst, i, num_sound,loc, file_name, age, sexe):
    new_sound = new_sound.concatenate([new_sound, current_sound])
    i += 1
    while call(new_sound, "Get total duration") < TARGET_DUR and i < len(file_lst):
        current_sound = read_files(file_lst[i])
        if not current_sound:
            i += 1
            continue
        new_sound = new_sound.concatenate([new_sound, current_sound])
        i += 1
    if call(new_sound, "Get total duration") > TARGET_DUR:
        new_sound = adjust_duration_to_target(new_sound, num_sound,loc, file_name, age, sexe)
    else:
        new_sound.save(f"../Corpus4Sec/PTSVOX_4Sec/{sexe}/{age}/{loc}/{file_name}_{num_sound}.wav", "WAV")
        temp = parselmouth.Sound(file_lst[0])
        new_sound = temp.extract_part(
            0, 0.01, parselmouth.WindowShape.RECTANGULAR, 1, False
        )
    return i - 1, new_sound

def split_corpus(path,sexe,age,loc):
    file_lst = glob.glob(path)
    if file_lst != []:
        i = 0
        num_sound = 0
        temp = parselmouth.Sound(file_lst[0])
        new_sound = temp.extract_part(
            0, 0.01, parselmouth.WindowShape.RECTANGULAR, 1, False
        )
        while i < len(file_lst):
            sound = read_files(file_lst[i])
            file_name = file_lst[i].split("/")[-1]
            file_name = "_".join(file_name.split("_")[:-1])
            duration_current = call(sound, "Get total duration") + call(
                new_sound, "Get total duration"
            )
            if duration_current == TARGET_DUR:
                sound.save(f"../Corpus4Sec/PTSVOX_4Sec/{sexe}/{age}/{loc}/{file_name}_{num_sound}.wav", "WAV")
            elif duration_current < TARGET_DUR:
                i, new_sound = add_files_until_target(
                    new_sound, sound, file_lst, i, num_sound, loc,file_name, age, sexe
                )
            elif duration_current > TARGET_DUR:
                new_sound = new_sound.concatenate([new_sound, sound])
                new_sound = adjust_duration_to_target(new_sound, num_sound,loc,file_name, age ,sexe)
            num_sound += 1
            i += 1
    else :
        print(f"Dossier vide : {loc} ")
        return
            
def main():
    folder_lst = glob.glob("PTSVOX_cut/*/*/*/")
    nb_folder = len(folder_lst)
    processed = 0
    for folder in folder_lst :
        sexe = folder.split("/")[1]
        age_cat = folder.split("/")[2]
        loc = folder.split("/")[3]

        print(f"Processing {folder}... ({processed}/{nb_folder})")
        if not os.path.exists(f"../Corpus4Sec/PTSVOX_4Sec/{sexe}/{age_cat}/{loc}"):
            os.mkdir(f"../Corpus4Sec/PTSVOX_4Sec/{sexe}/{age_cat}/{loc}")
            path = f"{folder}/*.wav"
            split_corpus(path,sexe,age_cat,loc)
            print(f"{folder} Folder split")
            processed += 1
        print(f"{folder} already processed")
        processed += 1
    
if __name__ == "__main__" :
    main()

