#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:48:36 2024

@author: orane
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

full_df = pd.read_csv("ESLO2_synthesis_acoustic_measures.csv")
df_1015 = full_df.loc[full_df["fichier"] == "labise_1015"]
print(df_1015)
full_df = full_df.loc[full_df["fichier"] != "labise_1015"]


def get_age_cat(df):
    old = df[df["classe_age"] == "old"]
    young = df[df["classe_age"] == "young"]
    return old, young

def get_descriptor_name(descriptor):
    if descriptor == "COG" :
        return "COG (Hz)"
    elif descriptor == "harmonicity":
        return "HNR"
    elif descriptor == "spectral_tilt":
        return "Pente Spectrale (dB)"
    elif descriptor == "f0" :
        return "F0 (Hz)"
    elif descriptor == "CPP" :
        return "CPP (dB)"

    
def make_plot(descriptor):
    name = get_descriptor_name(descriptor)
    
#####################################################################################################################
####################################FEMMES###########################################################################
    
    full_df_old_femme, full_df_young_femme = get_age_cat(full_df)
    full_measures_old_femme = full_df_old_femme[descriptor].dropna()
    full_measures_young_femme = full_df_young_femme[descriptor].dropna()
    full_measures_1015 = df_1015[descriptor].dropna()
    stderr_full_young_femme = full_measures_young_femme.std() / np.sqrt(len(full_measures_young_femme))
    stderr_full_old_femme = full_measures_old_femme.std() / np.sqrt(len(full_measures_old_femme))
    stderr_full_1015 = full_measures_1015.std() / np.sqrt(len(full_measures_1015))

    
#####################################################################################################################
######################################################################################################################
    fig,ax = plt.subplots(figsize=(12, 10))
    
    categories = ["<30", ">60", "1015 (73 ans)"]
    x_femme = np.arange(len(categories))
    
    data_femme = [full_measures_young_femme.mean(), full_measures_old_femme.mean(),full_measures_1015.mean()]
    stderr_femme = [stderr_full_young_femme, stderr_full_old_femme,stderr_full_1015]
    colors = ["tab:red", "tab:red", "tab:orange"]
    ax.bar(x_femme, data_femme, 0.5, label='Women', color=colors, yerr=stderr_femme, capsize=5)
    ax.set_xticks(x_femme)
    ax.set_xticklabels(categories)
    ax.set_title(f"{name} - Tous phonèmes")
    ax.set_ylabel(f"{name}")
    ax.set_xlabel("locuteurs")
    plt.grid()

    

    plt.tight_layout(rect=[0, 0.05, 1, 1])  
    plt.savefig(f"plots/comparison_plots/{descriptor}_1015_comparison.png")
    plt.show()
    
descriptors = ["CPP", "harmonicity", "COG", "f0", "spectral_tilt"]
for descriptor in descriptors :
    make_plot(descriptor)