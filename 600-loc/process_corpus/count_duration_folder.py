#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:25:47 2024

@author: odufour
"""
import glob 
import csv
import parselmouth
from parselmouth.praat import call
import glob
import csv
import os
from my_minipack.loading import ft_progress

lst_files = glob.glob("../../corpus_orfeo/femme/old/Mira/*.wav")

total_duration = 0
for file in lst_files :
    sound = parselmouth.Sound(file)
    duration = call(sound,"Get total duration")
    if duration > 10 :
        print(file, duration)
    total_duration += duration

print(total_duration)