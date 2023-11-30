#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:38:35 2023

@author: orane
"""

import pandas as pd

def convert_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds


df = pd.read_csv('../module_diachronie/metadonnees_diachronie.csv')


df['time_loc_seconds'] = df['time_loc'].apply(convert_to_seconds)


total_time_all = df['time_loc_seconds'].sum()


total_time_vieux = df[df['age'] == 'vieux']['time_loc_seconds'].sum()

total_time_jeune = df[df['age'] == 'jeune']['time_loc_seconds'].sum()


def convert_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


print("Total Recording Time for All Locutors:", convert_to_hms(total_time_all))
print("Total Recording Time for 'Vieux' Locutors:", convert_to_hms(total_time_vieux))
print("Total Recording Time for 'Jeune' Locutors:", convert_to_hms(total_time_jeune))