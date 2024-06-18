#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:43:54 2024

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


TARGET_DUR = 4

def adjust_duration_to_target(current_sound, num_sound,loc, file_name, age, sexe):
    duration_time = call(current_sound, "Get total duration")
    if duration_time < TARGET_DUR:
        print(f"error at extract {num_sound}")
    right_part = current_sound.extract_part(
        0, TARGET_DUR, parselmouth.WindowShape.RECTANGULAR, 1, False
    )
    right_part.save(f"../Fabiole2_4Sec/{sexe}/{age}/{loc}/{file_name}_{num_sound}.wav", "WAV")
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
        new_sound.save(f"./Fabiole2_4Sec/{sexe}/{age}/{loc}/{file_name}_{num_sound}.wav", "WAV")
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
                sound.save(f"../Fabiole2_4Sec/{sexe}/{age}/{loc}/{file_name}_{num_sound}.wav", "WAV")
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
    metadata = load_metadata("speakers.csv")
    folder_lst = glob.glob("../../corpus_fabiole2_part1/*")
    nb_folder = len(folder_lst)
    processed = 0
    lst_loc = [row["ID"] for row in metadata]
    for folder in ft_progress(folder_lst) :
        loc = folder.split("/")[-1]
        if loc not in lst_loc :
            print("Loc pas présent dans les métadonnées {loc}")
        else :
            for row in metadata :
                sexe = "homme" if row["Sexe"] == "H" else "femme"
                age_cat = get_age_cat(row["age"])
                name_loc = row["ID"]
                if loc == name_loc and age_cat:
                    if not os.path.exists(f"../Fabiole2_4Sec/{sexe}/{age_cat}/{loc}"):
                        os.mkdir(f"../Fabiole2_4Sec/{sexe}/{age_cat}/{loc}")
                        path = f"{folder}/*.wav"
                        split_corpus(path,sexe,age_cat,loc)

    
if __name__ == "__main__" :
    main()
