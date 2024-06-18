#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 13:37:43 2024

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

def cut_every4sec(file, loc_file,loc, age_cat , sexe):
    sound = parselmouth.Sound(file)
    duration_sound = call(sound, "Get total duration")
    start = 0
    end = 4
    num_file = 0
    while start <= duration_sound :
        sound_4sec = sound.extract_part(start, end, parselmouth.WindowShape.RECTANGULAR, 1, False)
        sound_4sec.save(f"../commonvoice_4Sec/{sexe}/{age_cat}/{loc}/{loc_file}_{num_file}.wav", "WAV")
        num_file += 1
        start += 4
        end += 4

        
print(os.path.exists("../Corpus4Sec/commonvoice_4Sec/"))
def main():
    lst_files = glob.glob("../../commonvoice_cat/*/*/*/*.wav")
    for file in ft_progress(lst_files) :
        loc_file = file.split("/")[-1]
        loc_name = file.split("/")[5]
        sexe = file.split("/")[3]
        age_cat = file.split("/")[4]
       
        if not os.path.exists(f"../commonvoice_4Sec/{sexe}/{age_cat}/{loc_name}/"):
            os.mkdir(f"../commonvoice_4Sec/{sexe}/{age_cat}/{loc_name}")
                    
        cut_every4sec(file, loc_file, loc_name, age_cat, sexe)
        
                
        
main()