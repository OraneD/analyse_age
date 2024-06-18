#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:54:03 2024

@author: odufour
"""
import pandas as pd
import matplotlib.pyplot as plt

full_df = pd.read_csv("ESLO2_acoustic_measures_all.csv")
labial_a = pd.read_csv("labial_a.csv")
a_pause = pd.read_csv("a_pause.csv")
phoneme_a = pd.read_csv("phoneme_a.csv")



def get_by_sexe(df, sexe):
    return df[df["sexe"] == sexe]

def get_all_df(sexe):
    full_df_split = get_by_sexe(full_df, sexe)
    labial_a_split = get_by_sexe(labial_a,sexe)
    a_pause_split = get_by_sexe(a_pause, sexe)
    phoneme_a_split = get_by_sexe(phoneme_a,sexe)
    return full_df_split, labial_a_split, a_pause_split, phoneme_a_split


def get_age_cat(df):
    old = df[df["classe_age"] == "old"]
    mid = df[df["classe_age"] == "mid"]
    young = df[df["classe_age"] == "young"]
    return old, mid, young

def get_descriptor_name(descriptor):
    if descriptor == "COG" :
        return "COG (Hz)"
    elif descriptor == "harmonicity":
        return "HNR"
    elif descriptor == "spectral_tilt":
        return "Spectral Tilt (dB)"
    elif descriptor == "f0" :
        return "F0 (Hz)"
    elif descriptor == "CPP" :
        return "CPP (dB)"

    
def make_plot(descriptor, sexe):
    name = get_descriptor_name(descriptor)
    
    full_df_split, labial_a_split, a_pause_split, phoneme_a_split = get_all_df(sexe)
    full_df_old, full_df_mid, full_df_young = get_age_cat(full_df_split)
    labial_a_old,labial_a_mid,labial_a_young = get_age_cat(labial_a_split)
    a_pause_old, a_pause_mid, a_pause_young = get_age_cat(a_pause_split)
    phoneme_a_old, phoneme_a_mid, phoneme_a_young = get_age_cat(phoneme_a_split)
    
    full_measures_old = full_df_old[descriptor].dropna()
    full_measures_mid = full_df_mid[descriptor].dropna()
    full_measures_young = full_df_young[descriptor].dropna()
    
    labial_a_measures_old = labial_a_old[descriptor].dropna()
    labial_a_measures_mid = labial_a_mid[descriptor].dropna()
    labial_a_measures_young = labial_a_young[descriptor].dropna()
    
    a_pause_measures_old = a_pause_old[descriptor].dropna()
    a_pause_measures_mid = a_pause_mid[descriptor].dropna()
    a_pause_measures_young = a_pause_young[descriptor].dropna()
    
    phoneme_a_measures_old = phoneme_a_old[descriptor].dropna()
    phoneme_a_measures_mid = phoneme_a_mid[descriptor].dropna()
    phoneme_a_measures_young = phoneme_a_young[descriptor].dropna()
    
    
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharey="row")
    
    axs[0,0].boxplot([full_measures_old, full_measures_mid, full_measures_young],
                   labels=[">60", "30>=60", "<30"],
                   showfliers=False) 
    axs[0,0].set_title(f"{name} - Tout")
    axs[0,0].set_ylabel(f"{name}")
    axs[0,0].set_xlabel("locuteurs")
    
    axs[0,1].boxplot([phoneme_a_measures_old, phoneme_a_measures_mid, phoneme_a_measures_young],
                   labels=[">60", "30>=60", "<30"],
                   showfliers=False)
    axs[0,1].set_title(f"{name} - /a/")
    axs[0,1].set_ylabel(f"{name}")
    axs[0,1].set_xlabel("locuteurs")
    
    axs[1,0].boxplot([labial_a_measures_old, labial_a_measures_mid, labial_a_measures_young],
                   labels=[">60", "30>=60", "<30"],
                   showfliers=False)
    axs[1,0].set_title(f"{name} - labial - /a/")
    axs[1,0].set_ylabel(f"{name}")
    axs[1,0].set_xlabel("locuteurs")
    
    axs[1,1].boxplot([a_pause_measures_old, a_pause_measures_mid, a_pause_measures_young],
                   labels=[">60", "30>=60", "<30"],
                   showfliers=False)
    axs[1,1].set_title(f"{name} - /a/ - pause")
    axs[1,1].set_ylabel(f"{name}")
    axs[1,1].set_xlabel("locuteurs")
    
    
    
    plt.suptitle(f"{name} par sexe et catégorie d'âge - Hommes", fontsize=16, y=1.05)
    plt.tight_layout()
    plt.show()
    
descriptors = ["CPP", "harmonicity", "COG", "f0", "spectral_tilt"]
for descriptor in descriptors :
    make_plot(descriptor, "homme")
