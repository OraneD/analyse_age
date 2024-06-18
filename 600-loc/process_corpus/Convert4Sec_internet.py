#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:11:18 2024

@author: odufour
"""
import csv
import parselmouth
from parselmouth.praat import call
import glob
import csv
import os
import librosa
import soundfile as sf
from my_minipack.loading import ft_progress

def read_files(file):
    
        return parselmouth.Sound(file)
def resample(file, new_sr):
    sound_file, sr = librosa.load(file, sr=None)
    sound_resampled = librosa.resample(sound_file, orig_sr=sr, target_sr=new_sr)
    sf.write(file, sound_resampled, new_sr)

def concatenate_corpus(path):
    file_lst = glob.glob(path)
    temp = parselmouth.Sound(file_lst[0])
    sample_rate = int(call(temp, "Get sampling frequency"))
    print(f"Sample rate {sample_rate}")
    new_sound = temp.extract_part(
        0, 0.01, parselmouth.WindowShape.RECTANGULAR, 1, False
    )
    print("Concatenating sounds...")
    for file in ft_progress(file_lst):
        sound = read_files(file)
        if int(call(sound, "Get sampling frequency")) != sample_rate :
            print("yes")
            resample(file,sample_rate)
            sound = read_files(sound)
        new_sound = new_sound.concatenate([new_sound,sound])
    duration = call(new_sound,"Get total duration")
    print(f"Folder concatenated : duration : {duration}")
    return new_sound

def cut_every4sec(full_sound,loc, age_cat , sexe):
    duration_sound = call(full_sound, "Get total duration")
    start = 0
    end = 4
    num_file = 0
    print("Cutting Sound.....")
    while start <= duration_sound :
        sound_4sec = full_sound.extract_part(start, end, parselmouth.WindowShape.RECTANGULAR, 1, False)
        sound_4sec.save(f"../internet_4Sec/{sexe}/{age_cat}/{loc}/{loc}_4Sec_{num_file}.wav", "WAV")
        num_file += 1
        start += 4
        end += 4
            
def main():
    folder_lst = glob.glob("../../corpus_internet/*/*/*")
    for folder in ft_progress(folder_lst):
        loc = folder.split("/")[-1]
        age_cat = folder.split("/")[-2]
        sexe = folder.split("/")[-3]
        if not os.path.exists(f"../internet_4Sec/{sexe}/{age_cat}/{loc}"):
            os.mkdir(f"../internet_4Sec/{sexe}/{age_cat}/{loc}")
            path = f"{folder}/*.wav"
            full_sound = concatenate_corpus(path)
            cut_every4sec(full_sound,loc,age_cat,sexe)

    
if __name__ == "__main__" :
    main()
