#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:43:50 2024

@author: odufour
"""

import csv
import parselmouth
from parselmouth.praat import call
import tgt
import glob
import os
from my_minipack.loading import ft_progress


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

def get_f0(sound,interval):
    manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
    start_time = interval.start_time
    end_time = interval.end_time
    mid = (end_time+start_time)/2
    pitch_tier = call(manipulation, "Extract pitch tier")
    pitch_current = call(pitch_tier,"Get value at time", mid)
    return pitch_current

def get_spectral_measures(sound, interval):
    start = interval.start_time
    end = interval.end_time
    label = interval.text if interval.text != "" else "_"
    mid = (end+start)/2
    duration = round((end-start)*1000)
    extract = call(sound,"Extract part", mid - 0.015, mid +0.015,"Kaiser2",1,"yes")
    spectre = call(extract, "To Spectrum", "yes")
    cog = call(spectre,"Get centre of gravity", 2)
    skew = call(spectre,"Get skewness", 2)
    spectral_tilt = call(spectre, "Get band energy difference", 0, 2000, 2000, 8000)
    return label, duration, cog, skew, spectral_tilt

def get_harmonicity(sound, interval):
    start = interval.start_time
    end = interval.end_time
    mid = (end+start)/2
    extract = call(sound,"Extract part", mid - 0.015, mid +0.015,"Kaiser2",1,"yes")
    harmonicity = call(extract, "To Harmonicity (cc)", 0.01, 75.0, 0.1, 1.0)
    #Paramètres To Harmonicity :
        #Time step (s)
        #Minimum pitch (Hz)
        #Silence treshold
        #Periods per window
    mean_hnr = call(harmonicity, "Get mean...", 0.0, 0.0)
    #Paramètres Get mean :
        #Time range(s) si 0.0, 0.0 = all
    return mean_hnr


def get_cepstral_peak_prominence(sound, interval):
    start = interval.start_time
    end = interval.end_time
    mid = (end+start)/2
    extract = call(sound,"Extract part", mid - 0.015, mid +0.015,"Kaiser2",1,"yes")
    powercepstrogram = call(extract, "To PowerCepstrogram", 60, 0.002,5000,50)
    #Paramètres To PowerCepstrogram :
        #Pitch floor (Hz)
        #Time step (s)
        #Maximum Frequency (Hz)
        #Pre-emphasis (Hz)
    cepstral_peak_prominence = call(powercepstrogram,"Get CPPS...","yes", 0.02, 0.0005, 60,330, 0.05, "parabolic", 0.001, 0.05, "exponential decay", "robust slow")
    #Paramètres Get CPPS : 
        #Substract trand before smoothing (yes or no)
        #Time averaging window (s)
        #Quefrency averaging window (s)
        #Peak search pitch range (Hz) -> 60,330 here
        #Tolerance (0-1)
        #Interpolation -> str("none","parabolic","cubic","sinc70","sinc700")
        #Trend line quefrency range (s) -> 0.001, 0.05 here
        #Trend type -> str("EXponential decay", "Straight")
        #Fit method -> str("Robust Slow", "Least squares", "robust")        
    return cepstral_peak_prominence

def get_age_cat(age):
    if age == "vieux":
        return "old"
    elif int(age) < 30 :
        return "young"
    elif int(age) >= 30 and int(age) <= 60 :
        return "mid"
    elif int(age) > 60 :
        return "old"


def main():
    files = load_files("../corpus_cross_val/*/*/*/*.wav")
    metadonnees = load_ages("../../metadonnees_ESLO2_ENT_ENTJEUN.csv")
    with open("ESLO2_acoustic_measures.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["fichier","sexe", "age","classe_age", "phoneme", "left" ,"right", "duration","COG", "spectral_tilt", "f0", "harmonicity", "CPP"])
        for file in ft_progress(files) :
            basename = get_basename(file)
            for loc in metadonnees :
                if loc["directory"] == "_".join(basename.split("_")[:3]):
                    age = loc["age"]
                    classe_age = get_age_cat(age)
                    sexe = loc["sexe"]
            if os.path.isfile(file.replace(".wav", ".TextGrid")):
                sound, textgrid = read_files(file, file.replace(".wav", ".TextGrid"))
                intervals_phones, interval_words = extract_interval_tier(textgrid)
                for i, interval in enumerate(intervals_phones) :
                    label, duration, cog, skew, spectral_tilt = get_spectral_measures(sound,interval)
                    f0 = get_f0(sound,interval)
                    mean_hnr = get_harmonicity(sound, interval)
                    cepstral_peak_prominence = get_cepstral_peak_prominence(sound,interval)
                    contexte_gauche = intervals_phones[i-1].text if i != 0 else "None"
                    contexte_gauche = "_" if contexte_gauche == "" else contexte_gauche
                    if len(intervals_phones) > 1 :
                        if i < len(intervals_phones) -1 :
                            contexte_droit = intervals_phones[i+1].text 
                        else :
                            contexte_droit = "None"
                    else : 
                        contexte_droit = "None"
                    contexte_droit = "_" if contexte_droit == "" else contexte_droit
                    writer.writerow([basename,sexe,age,classe_age,label, contexte_gauche, contexte_droit,duration, cog,spectral_tilt,f0,mean_hnr, cepstral_peak_prominence])
                
            
        
main()