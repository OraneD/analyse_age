#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 14:32:39 2024

@author: orane
"""

import pandas as pd
import csv

data = pd.read_csv("corpus_description.csv")
with open("lst_loc", "r") as file :
    text = file.readlines()
    lst_loc = [x.strip() for x in text]

df_filtre = data[data['fichier'].str.contains('|'.join(lst_loc))]
df_filtre.to_csv("description_loc_corpus.csv", index=False)
