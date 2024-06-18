#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:06:09 2024

@author: odufour
"""
import csv
import parselmouth
from parselmouth.praat import call
import glob
import csv
import os

def load_metadata(file):
    with open(file, "r", encoding="iso-8859-1") as f :
        reader=csv.DictReader(f)
        return[*reader]
   # return [*csv.DictReader(open(file))]

def get_age_cat(age):
    if int(age) < 30 :
        return "young"
    if int(age) >= 30 and int(age) <= 60 :
        return "mid"
    else :
        print("LOCUTEUR PLUS DE 60 ANS")

def cut_every4sec(file, loc, age_cat , sexe, session, recording_type):
    sound = parselmouth.Sound(file)
    duration_sound = call(sound, "Get total duration")
    start = 0
    end = 4
    num_file = 0
    while start <= duration_sound :
        sound_4sec = sound.extract_part(start, end, parselmouth.WindowShape.RECTANGULAR, 1, False)
        sound_4sec.save(f"../Corpus4Sec/PTSVOX_4sec/{sexe}/{age_cat}/{loc}/{loc}_{session}_{recording_type}_{num_file}.wav", "WAV")
        num_file += 1
        start += 4
        end += 4

        


def main():
    metadata = load_metadata("base_donnees_perso_ptsvox_sansnom.csv")
    lst_files = glob.glob("44100_mono/*.wav")
    nb_files = len(lst_files)
    i = 1
    for file in lst_files :
        loc_file = file.split("/")[1].split("_")[1]
        num_session = file.split("/")[1].split("_")[3]
        record_type = file.split("/")[1].split("_")[4]
        lst_loc_meta = [row["XX"].split("_")[1]  for row in metadata]
        if loc_file not in lst_loc_meta :
            print(f"Locuteur pas présent dans les métadonnées : {loc_file}")
            break
        for row in metadata :

            loc = row["XX"].split("_")[1]
            age_cat = get_age_cat(row["age"])
            sexe = "homme" if row["H/F"] == "H" else "femme"

            
            if loc_file == loc:
                if not os.path.exists(f"../Corpus4Sec/PTSVOX_4sec/{sexe}/{age_cat}/{loc}/"):
                    os.mkdir(f"../Corpus4Sec/PTSVOX_4sec/{sexe}/{age_cat}/{loc}")
                    
                print(f"Processing {file}...")
                cut_every4sec(file, loc, age_cat, sexe, num_session, record_type)
                print(f"{file} Processed ! ({i}/{nb_files})")
             
        
        i += 1
                
        
main()