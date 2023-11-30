#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 22:02:23 2023

@author: orane
"""

import parselmouth
from parselmouth.praat import call
import tgt
import glob
import csv
import os

def get_file_lst(path_folder):
    return glob.glob("../../" + path_folder)

def load_metadata(file):
    return [*csv.DictReader(open(file))]     

def extract_interval_tier(textgrid):
    return textgrid.get_tier_by_name("phones")


def process_files(sound,interval):
       start_time = interval.start_time
       end_time = interval.end_time
       label = interval.text
       if label == "" :
           label = "_"
       
       mid = (end_time+start_time)/2
       duration = round((end_time-start_time)*1000)
       extract = call(sound,"Extract part", mid - 0.015, mid +0.015,"Kaiser2",1,"yes")
       spectre = call(extract, "To Spectrum", "yes")
       cog = call(spectre,"Get centre of gravity", 2)
       skew = call(spectre,"Get skewness", 2)

       return label, duration, cog, skew
       


def read_files(file):
    path_wav =  file
    path_textgrid = "../../module_diachronie/diachronie_mfa/"  + "".join(file.split("/")[4]) + "/" + "".join(file.split("/")[4]) + "_aligned/" + "".join(file.split("/")[5].replace(".wav", ".TextGrid"))
    print(path_wav)
    print(path_textgrid)
    if os.path.isfile(path_textgrid):
        sound = parselmouth.Sound(path_wav)
        textgrid = tgt.io.read_textgrid(path_textgrid)
        return sound, textgrid
    else :
        return False

    

def main() : 
    with open("resultats_corpus_diachronie.csv", "w", newline='') as csvfile :
        writer = csv.writer(csvfile)
        writer.writerow(["dossier", 
                      "fichier",
                      "age", 
                      "sexe", 
                      "niveau_etude", 
                      "categorie_professionnelle", 
                      "phoneme", 
                      "duree", 
                      "cog", 
                      "skew"])

        metadata = (load_metadata("../../module_diachronie/metadonnees_diachronie.csv"))
        len_folders = len(metadata)
        for i, row in enumerate(metadata) :
            missing_file = 0
            folder = row["directory"]
            sexe = row["sexe"]
            age = row["age"]
            niveau_etude = row["niveau_etude"]
            categorie_professionnelle = row["categorie_professionnelle"]
            
            print(f"Folder : {folder} ({i + 1}/{len_folders})")
            file_lst = get_file_lst(f"module_diachronie/diachronie_mfa/{folder}/*.wav")
            print(file_lst)
            nb_files = len(file_lst)
            for file in file_lst :
                if read_files(file) != False :
                    sound, textgrid = read_files(file)
                    tier = extract_interval_tier(textgrid)
                    for interval in tier.intervals :
                        label, duration, cog, skew = process_files(sound,interval)
                        writer.writerow([folder,
                                      file.split("/")[5],
                                      age,
                                      sexe,
                                      niveau_etude,
                                      categorie_professionnelle,
                                      label,
                                      duration,
                                      cog,
                                      skew])
                else :
                    missing_file += 1
                    continue
            print(f"Completed - {missing_file}/{nb_files} missing files")
        


if __name__ == "__main__" :
    main()

    
