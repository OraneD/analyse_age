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

def create_big_tg(path,basename):
    file_lst = get_file_lst(path)
    big_tg = read_files(file_lst[0])[1]
    for file in file_lst[1:]:
        sound, textgrid = read_files(file)
        if not textgrid:
            continue
        big_tg = tgt.util.concatenate_textgrids([big_tg, textgrid])
    final = tgt.io.export_to_long_textgrid(big_tg)
    write_textgrid(final,f"../{basename}/{basename}_big_tg.TextGrid" )

def write_textgrid(textgrid, path):
    with open(path, "w") as file:
        file.write(textgrid)
        



