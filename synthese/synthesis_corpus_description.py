#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:03:06 2024

@author: orane
"""

"""
Created on Fri Jan 19 16:32:59 2024

@author: orane
"""

import csv
import parselmouth
from parselmouth.praat import call
import tgt
import glob
import os

def load_ages(metadonnees):
    with open(metadonnees, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
        return(data)
    
def load_files(path):
    return glob.glob(path)

def get_basename(file):
    return file.split("/")[-1].split(".")[0]

def extract_interval_tier(textgrid):
    return textgrid.get_tier_by_name("phones"), textgrid.get_tier_by_name("words")

def read_files(path_wav,path_textgrid):
        sound = parselmouth.Sound(path_wav)
        textgrid = tgt.io.read_textgrid(path_textgrid, include_empty_intervals=True)
        return sound, textgrid

def process_files(sound,intervals):
    duree_totale = call(sound,"Get total duration")
    nb_pause = 0
    nb_orales = 0
    nb_nasales = 0
    nb_occ = 0
    nb_sonantes = 0
    nb_fricatives = 0
    nb_cons_nasales = 0
    nb_semi_voy = 0
    nb_intervals = len(intervals)
    duree_intervals = []
    duree_pause = 0
    for interval in intervals : 
        start = interval.start_time
        end = interval.end_time
        duree_interval = end - start
        duree_intervals.append(duree_interval)
        if interval.text in [" ", ""]:
            duree_pause += duree_interval
            nb_pause += 1
        if interval.text in voyelles_orales :
            nb_orales += 1
        elif interval.text in voyelles_nasales :
            nb_nasales += 1
        elif interval.text in cons_occ :
            nb_occ += 1
        elif interval.text in cons_sonantes :
            nb_sonantes += 1
        elif interval.text in cons_fricatives :
            nb_fricatives += 1
        elif interval.text in cons_nasales :
            nb_cons_nasales += 1
        elif interval.text in semi_voy :
            nb_semi_voy += 1
    duree_sans_pause = duree_totale - duree_pause
    duree_moyenne = sum(duree_intervals)/nb_intervals
    articulation_rate =(( nb_orales + nb_nasales + nb_occ + nb_sonantes + nb_fricatives + nb_cons_nasales + nb_semi_voy) - nb_pause) / duree_sans_pause
    return duree_totale, duree_moyenne, nb_pause, nb_orales, nb_nasales, nb_occ, nb_sonantes, nb_fricatives, nb_cons_nasales, nb_semi_voy, articulation_rate


def get_mean_f0(sound,intervals):
    manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
    pitch = 0
    nb_voyelles = 0
    for interval in intervals :
       label = interval.text
       if label in voyelles_orales :
           nb_voyelles += 1
           start_time = interval.start_time
           end_time = interval.end_time
           mid = (end_time+start_time)/2
           duration = round((end_time-start_time)*1000)
           pitch_tier = call(manipulation, "Extract pitch tier")
           pitch_current = call(pitch_tier,"Get value at time", mid)
           pitch += pitch_current
    return pitch/nb_voyelles if nb_voyelles != 0 else None

def get_words_number(intervals_words):
    nb_words = 0
    for interval in intervals_words :
        if interval.text not in ["", " ", "_", "spn", "euh"]:
            nb_words += 1
    return nb_words

def get_pente(sound):
    spectre = call(sound,'To Spectrum', "yes")
    pente = call(spectre, "Get band energy difference", 0, 2000, 2000, 8000)
    return pente
    
    

voyelles_orales = ["a", "ɑ", "e", "ɛ", "i", "œ", "ø", "o", "ɔ", "ə", "ɛː", "u", "y"]
voyelles_nasales = ["ɑ̃", "œ̃", "ɛ̃", "ɔ̃"]
cons_occ = ["p", "t", "k", "b", "d", "g"]
cons_sonantes = ["ʁ", "l", "ʎ"]
cons_fricatives = ["s", "ʃ","v", "z", "ʒ", "f"]
cons_nasales = ["m", "n", "ŋ", "ɲ"]
semi_voy = ["j", "w", "ɥ"]

def main():
    files = load_files("../corpus_cross_val/*/*/*/*.wav")
    metadonnees = load_ages("../../metadonnees_ESLO2_ENT_ENTJEUN.csv")
    with open("corpus_description_mid.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["fichier","sexe", "age","classe_age", "duree", "duree_moy_segment", "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale", "nb_occlusive", "nb_sonante", "nb_fricative", "nb_nasale", "nb_semi-voyelle", "moy_F0_voyelles", "articulation_rate", "nb_mots", "pente"])
        for file in files :
            classe_age = file.split("/")[3]
            sexe= file.split("/")[2]
            basename = get_basename(file)
            for loc in metadonnees :
                if loc["directory"] == "_".join(basename.split("_")[:3]):
                    age = loc["age"]
            if os.path.isfile(file.replace(".wav", ".TextGrid")):
                sound, textgrid = read_files(file, file.replace(".wav", ".TextGrid"))
                intervals_phones, interval_words = extract_interval_tier(textgrid)
                duree_totale, duree_moyenne, nb_pause, nb_orales, nb_nasales, nb_occ, nb_sonantes, nb_fricatives, nb_cons_nasales, nb_semi_voy, articulation_rate = process_files(sound,intervals_phones)
                mean_pitch_voyelles = get_mean_f0(sound,intervals_phones)
                nb_words = get_words_number(interval_words)
                pente = get_pente(sound)
                writer.writerow([basename,sexe,age,classe_age,duree_totale, duree_moyenne, nb_pause, nb_orales, nb_nasales, nb_occ, nb_sonantes, nb_fricatives, nb_cons_nasales, nb_semi_voy, mean_pitch_voyelles, articulation_rate, nb_words, pente])
                
            
        
main()