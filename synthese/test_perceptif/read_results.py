#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 12:12:24 2024

@author: odufour
"""

import pandas as pd
import csv

def load_csv(metadonnees):
    with open(metadonnees, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
        return(data)

data = load_csv("experiment_data/data.csv")

def read_expe_file(file):
    df = pd.DataFrame()
    with open(file, "r") as f :
        lines = [x.strip() for x in f.readlines()]
        exp = [x.split() for x in lines]
    df["age_locuteur"] = [x[0] for x in exp]
    df["fichier"] = [x[1] for x in exp]
    df["reponse"] = [x[2] for x in exp]
    df["tempsReponse"] = [x[3] for x in exp]
    df["statusReponse"] = [x[4] for x in exp]
    return df
    
df_final = pd.DataFrame()

for row in data :
    exp_file = row["expe_1"] if row["expe_1"] != "" else "pas de fichier"
    if exp_file != "pas de fichier":
        df = read_expe_file(f"experiment_data/{exp_file}")
        df_final = pd.concat([df_final, df])

grouped = df_final.groupby(['fichier', 'reponse'])

result = grouped.agg(
    age_locuteur=('age_locuteur', 'first'),
    nb_reponses=('reponse', 'size'),
).reset_index()

print(result)
result.to_csv("result_test.csv")
    
