#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:57:29 2024

@author: orane
"""

import glob
import os
import numpy as np
import csv
from scipy.signal import find_peaks

from cepstral_modulation_example_original import get_MFCCS_change
from my_minipack.loading import ft_progress


def load_ages(metadonnees):
    with open(metadonnees, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
        return(data)

def get_age_cat(age):
    if age == "vieux":
        return "old"
    elif int(age) < 30 :
        return "young"
    elif int(age) >= 30 and int(age) <= 60 :
        return "mid"
    elif int(age) > 60 :
        return "old"
    
folders = glob.glob("../corpus_mfa_1channel/*")
metadonnees = load_ages("../metadonnees_ESLO2_ENT_ENTJEUN.csv")

for row in ft_progress(metadonnees) :
    print()
    dir_name = row["directory"]
    age = row["age"]
    age_cat = get_age_cat(age)
    sexe = row["sexe"]
    files = glob.glob(f"../corpus_mfa_1channel/{dir_name}/*.wav")
    if not os.path.isdir(f"loc_modulation/{dir_name}"):
        os.mkdir(f"loc_modulation/{dir_name}")
        print(f"Processing {dir_name}...")
        with open(f"loc_modulation/{dir_name}/{dir_name}_mean_spectralChange.csv", "w") as f:
            f.write("locuteur,sexe,age,age_cat,file,mean_SpectralChange,mean_positiv_Peaks, mean_supmedian_Peaks\n")
            for file in ft_progress(files):
                try:
                    file_name = file.split("/")[-1]
                    save_name = file_name.replace(".wav", ".txt")
                    spectralChange,timeStamps = get_MFCCS_change(file)
                    #np.savetxt(f"loc_modulation/{dir_name}/{save_name}",spectralChange)
                    mean_spectralChange = np.mean(spectralChange, axis=0)
                    peaks , _ = find_peaks(spectralChange,height=0)
                    peak_values = spectralChange[peaks]
                    mean_peak_value=np.mean(peak_values)
                    median_peak_height = np.median(spectralChange[peaks])
                    filtered_peaks_indices = [peak for peak in peaks if spectralChange[peak] > median_peak_height and spectralChange[peak] > 0]
                    mean_median_peaks = np.mean(spectralChange[filtered_peaks_indices])

                    f.write(f"{dir_name},{sexe},{age},{age_cat},{file_name},{mean_spectralChange},{mean_peak_value},{mean_median_peaks}\n")
                except ValueError as e:
                   if "The length of the input vector x must be greater than padlen" in str(e):
                       print(f"Skipping {file_name} due to insufficient data length.")
                   else:
                       raise 
    else : 
        continue
#spectralChange,timeStamps = get_MFCCS_change("D:/dvd_dga_reste_ESTER/data/total_avec_et_sans_chunking/fait/19981209_0700_0800_franceinter_dga.wav")
#np.savetxt("output_19981209_0700_0800_franceinter_dga.txt",spectralChange)
