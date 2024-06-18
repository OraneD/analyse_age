#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 16:19:49 2024

@author: orane
"""
import parselmouth
from parselmouth.praat import call
import tgt
import glob
import csv
import os

from create_big_tg import create_big_tg
from cut_textgrid4 import split_textgrid

TARGET_DUR = 4


def get_file_lst(path_folder):
    return glob.glob("../../corpus_mfa_1channel/" + path_folder)


def load_metadata(file):
    return [*csv.DictReader(open(file))]


def extract_interval_tier(textgrid):
    return textgrid.get_tier_by_name("phones")


def get_basename(file):
    return file.split("/")[-1].replace(".wav", "")


def read_files(file):
    basename = get_basename(file)
    folder = "_".join(basename.split("_")[:3])
    path_wav = file
    path_textgrid = (
        "/".join(path_wav.split("/")[:4])
        + f"/{folder}_aligned/"
        + basename
        + ".TextGrid"
    )

    if os.path.isfile(path_textgrid):
        sound = parselmouth.Sound(path_wav)
        textgrid = tgt.io.read_textgrid(path_textgrid)
        return sound, textgrid
    else:
        return False, False


def add_files_until_target(new_sound, current_sound, file_lst, i, num_sound, basename):
    new_sound = new_sound.concatenate([new_sound, current_sound])
    i += 1
    while call(new_sound, "Get total duration") < TARGET_DUR and i < len(file_lst):
        current_sound, tg = read_files(file_lst[i])
        if not current_sound or not tg:
            i += 1
            continue
        new_sound = new_sound.concatenate([new_sound, current_sound])
        i += 1
    if call(new_sound, "Get total duration") > TARGET_DUR:
        new_sound = adjust_duration_to_target(new_sound, num_sound,basename)
    else:
        new_sound.save(f"../{basename}/{basename}_{num_sound}.wav", "WAV")
        temp = parselmouth.Sound(file_lst[0])
        new_sound = temp.extract_part(
            0, 0.01, parselmouth.WindowShape.RECTANGULAR, 1, False
        )
    return i - 1, new_sound


def adjust_duration_to_target(current_sound, num_sound,basename):
    duration_time = call(current_sound, "Get total duration")
    if duration_time < TARGET_DUR:
        print(f"error at extract {num_sound}")
    right_part = current_sound.extract_part(
        0, TARGET_DUR, parselmouth.WindowShape.RECTANGULAR, 1, False
    )
    right_part.save(f"../{basename}/{basename}_{num_sound}.wav", "WAV")
    return current_sound.extract_part(
        TARGET_DUR, duration_time, parselmouth.WindowShape.RECTANGULAR, 1, False
    )


def split_corpus(path,basename):
    file_lst = get_file_lst(path)
    i = 0
    num_sound = 0
    temp = parselmouth.Sound(file_lst[0])
    new_sound = temp.extract_part(
        0, 0.01, parselmouth.WindowShape.RECTANGULAR, 1, False
    )
    while i < len(file_lst):
        sound, textgrid = read_files(file_lst[i])
        if not sound or not textgrid:
            i += 1
            continue
        duration_current = call(sound, "Get total duration") + call(
            new_sound, "Get total duration"
        )
        if duration_current == TARGET_DUR:
            sound.save(f"../{basename}/{basename}_{num_sound}.wav", "WAV")
        elif duration_current < TARGET_DUR:
            i, new_sound = add_files_until_target(
                new_sound, sound, file_lst, i, num_sound, basename
            )
        elif duration_current > TARGET_DUR:
            new_sound = new_sound.concatenate([new_sound, sound])
            new_sound = adjust_duration_to_target(new_sound, num_sound,basename)
        num_sound += 1
        i += 1
        
def main():
    metadata = load_metadata("../../metadonnees_ESLO2_ENT_ENTJEUN.csv")
    for row in metadata:
        folder = row["directory"]
        print()
        print(f"Processing {folder}...")
        if not os.path.exists(f"../{folder}"):
            os.mkdir(f"../{folder}")
            path = f"{folder}/*.wav"
            split_corpus(path,folder)
            print(f"{folder} Folder split")
            create_big_tg(path,folder)
            print(f"{folder} big TextGrid Created")
            split_textgrid(f"../{folder}/{folder}_big_tg.TextGrid", folder)
            print(f"{folder} Split TextGrids created")
            print(f"{folder} Processed !")
            print()
        


if __name__ == "__main__":
    main()
