#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 21:31:44 2023

@author: orane
"""
import csv 
import pandas as pd

def convert_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def convert_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def count_age(file):
    df = pd.read_csv(file, delimiter = ",")
    print(df)
    df["age"] = pd.to_numeric(df["age"], errors='coerce')
    print("Valeurs manquantes dans 'age' après conversion:", df['age'].isna().sum())
    bins = [20, 30, 40, 50, 60, 70, 80, 90]
    labels = ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89']
    df['Tranche_d_age'] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    resultat = df.groupby('Tranche_d_age')["directory"].nunique()
    
    df['duree_loc_seconds'] = df['loc_duration(mm:ss)'].apply(convert_to_seconds)
    total_time_per_age_slice = df.groupby('Tranche_d_age')['duree_loc_seconds'].sum()
    total_time_per_age_slice = total_time_per_age_slice.apply(convert_to_hms)
    print(total_time_per_age_slice)
    print(resultat)



count_age("../metadonnees_ESLO2_ENT_ENTJEUN.csv")