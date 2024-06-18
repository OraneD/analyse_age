#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:13:52 2024

@author: odufour
"""

import glob
import os
import numpy as np
from cepstral_modulation_example_original import get_MFCCS_change
from my_minipack.loading import ft_progress


folders = glob.glob("../corpus_mfa_1channel/*")
for folder in ft_progress(folders) :
    print()
    dir_name = folder.split("/")[-1]
    files = glob.glob(f"{folder}/*.wav")
    if not os.path.isdir(f"loc_modulation/{dir_name}"):
        os.mkdir(f"loc_modulation/{dir_name}")
    print(f"Processing {dir_name}...")
    with open(f"loc_modulation/{dir_name}/{dir_name}_mean_maxPeak.csv", "w") as f:
        f.write("locuteur,mean_maxPeak\n")
        max_peaks = []
        for file in ft_progress(files):
            file_name = file.split("/")[-1]
            save_name = file_name.replace(".wav", ".txt")
            spectralChange,timeStamps = get_MFCCS_change(file)
            max_peak = np.max(spectralChange)
            max_peaks.append(max_peak)
        max_peaks = np.to_array(max_peaks)
        mean_maxPeak = np.mean(max_peaks, axis=0)
        f.write(f"{dir_name},{mean_maxPeak}\n")