#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 15:54:22 2024

@author: orane
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

    
def make_plot(descriptor):
    name = get_descriptor_name(descriptor)
    
#####################################################################################################################
####################################FEMMES###########################################################################
    
    full_df_split_femme, labial_a_split_femme, a_pause_split_femme, phoneme_a_split_femme = get_all_df("femme")
    full_df_old_femme, full_df_mid_femme, full_df_young_femme = get_age_cat(full_df_split_femme)
    labial_a_old_femme, labial_a_mid_femme, labial_a_young_femme = get_age_cat(labial_a_split_femme)
    a_pause_old_femme, a_pause_mid_femme, a_pause_young_femme = get_age_cat(a_pause_split_femme)
    phoneme_a_old_femme, phoneme_a_mid_femme, phoneme_a_young_femme = get_age_cat(phoneme_a_split_femme)
    
    full_measures_old_femme = full_df_old_femme[descriptor].dropna()
    full_measures_mid_femme = full_df_mid_femme[descriptor].dropna()
    full_measures_young_femme = full_df_young_femme[descriptor].dropna()
    
    labial_a_measures_old_femme = labial_a_old_femme[descriptor].dropna()
    labial_a_measures_mid_femme = labial_a_mid_femme[descriptor].dropna()
    labial_a_measures_young_femme = labial_a_young_femme[descriptor].dropna()
    
    a_pause_measures_old_femme = a_pause_old_femme[descriptor].dropna()
    a_pause_measures_mid_femme = a_pause_mid_femme[descriptor].dropna()
    a_pause_measures_young_femme = a_pause_young_femme[descriptor].dropna()
    
    phoneme_a_measures_old_femme = phoneme_a_old_femme[descriptor].dropna()
    phoneme_a_measures_mid_femme = phoneme_a_mid_femme[descriptor].dropna()
    phoneme_a_measures_young_femme = phoneme_a_young_femme[descriptor].dropna()
    
    stderr_full_young_femme = full_measures_young_femme.std() / np.sqrt(len(full_measures_young_femme))
    stderr_full_mid_femme = full_measures_mid_femme.std() / np.sqrt(len(full_measures_mid_femme))
    stderr_full_old_femme = full_measures_old_femme.std() / np.sqrt(len(full_measures_old_femme))
    
    
    stderr_phoneme_a_young_femme = phoneme_a_measures_young_femme.std() / np.sqrt(len(phoneme_a_measures_young_femme))
    stderr_phoneme_a_mid_femme = phoneme_a_measures_mid_femme.std() / np.sqrt(len(phoneme_a_measures_mid_femme))
    stderr_phoneme_a_old_femme = phoneme_a_measures_old_femme.std() / np.sqrt(len(phoneme_a_measures_old_femme))

    stderr_labial_a_young_femme = labial_a_measures_young_femme.std() / np.sqrt(len(labial_a_measures_young_femme))
    stderr_labial_a_mid_femme = labial_a_measures_mid_femme.std() / np.sqrt(len(labial_a_measures_mid_femme))
    stderr_labial_a_old_femme = labial_a_measures_old_femme.std() / np.sqrt(len(labial_a_measures_old_femme))
    
    stderr_a_pause_young_femme = a_pause_measures_young_femme.std() / np.sqrt(len(a_pause_measures_young_femme))
    stderr_a_pause_mid_femme = a_pause_measures_mid_femme.std() / np.sqrt(len(a_pause_measures_mid_femme))
    stderr_a_pause_old_femme = a_pause_measures_old_femme.std() / np.sqrt(len(a_pause_measures_old_femme))
    
#####################################################################################################################
###################################HOMMES############################################################################
    
    full_df_split_homme, labial_a_split_homme, a_pause_split_homme, phoneme_a_split_homme = get_all_df("homme")
    full_df_old_homme, full_df_mid_homme, full_df_young_homme = get_age_cat(full_df_split_homme)
    labial_a_old_homme, labial_a_mid_homme, labial_a_young_homme = get_age_cat(labial_a_split_homme)
    a_pause_old_homme, a_pause_mid_homme, a_pause_young_homme = get_age_cat(a_pause_split_homme)
    phoneme_a_old_homme, phoneme_a_mid_homme, phoneme_a_young_homme = get_age_cat(phoneme_a_split_homme)
    
    full_measures_old_homme = full_df_old_homme[descriptor].dropna()
    full_measures_mid_homme = full_df_mid_homme[descriptor].dropna()
    full_measures_young_homme = full_df_young_homme[descriptor].dropna()
    
    labial_a_measures_old_homme = labial_a_old_homme[descriptor].dropna()
    labial_a_measures_mid_homme = labial_a_mid_homme[descriptor].dropna()
    labial_a_measures_young_homme = labial_a_young_homme[descriptor].dropna()
    
    a_pause_measures_old_homme = a_pause_old_homme[descriptor].dropna()
    a_pause_measures_mid_homme = a_pause_mid_homme[descriptor].dropna()
    a_pause_measures_young_homme = a_pause_young_homme[descriptor].dropna()
    
    phoneme_a_measures_old_homme = phoneme_a_old_homme[descriptor].dropna()
    phoneme_a_measures_mid_homme = phoneme_a_mid_homme[descriptor].dropna()
    phoneme_a_measures_young_homme = phoneme_a_young_homme[descriptor].dropna()
    
    stderr_full_young_homme = full_measures_young_homme.std() / np.sqrt(len(full_measures_young_homme))
    stderr_full_mid_homme = full_measures_mid_homme.std() / np.sqrt(len(full_measures_mid_homme))
    stderr_full_old_homme = full_measures_old_homme.std() / np.sqrt(len(full_measures_old_homme))
    
    stderr_phoneme_a_young_homme = phoneme_a_measures_young_homme.std() / np.sqrt(len(phoneme_a_measures_young_homme))
    stderr_phoneme_a_mid_homme = phoneme_a_measures_mid_homme.std() / np.sqrt(len(phoneme_a_measures_mid_homme))
    stderr_phoneme_a_old_homme = phoneme_a_measures_old_homme.std() / np.sqrt(len(phoneme_a_measures_old_homme))
    
    stderr_labial_a_young_homme = labial_a_measures_young_homme.std() / np.sqrt(len(labial_a_measures_young_homme))
    stderr_labial_a_mid_homme = labial_a_measures_mid_homme.std() / np.sqrt(len(labial_a_measures_mid_homme))
    stderr_labial_a_old_homme = labial_a_measures_old_homme.std() / np.sqrt(len(labial_a_measures_old_homme))
    
    stderr_a_pause_young_homme = a_pause_measures_young_homme.std() / np.sqrt(len(a_pause_measures_young_homme))
    stderr_a_pause_mid_homme = a_pause_measures_mid_homme.std() / np.sqrt(len(a_pause_measures_mid_homme))
    stderr_a_pause_old_homme = a_pause_measures_old_homme.std() / np.sqrt(len(a_pause_measures_old_homme))

######################################################################################################################
######################################################################################################################
    fig, axs = plt.subplots(2, 2, figsize=(12, 10), sharey=True)
    
    categories = ["<30", "30-60", ">60"]
    x_femme = np.arange(len(categories)) * 0.1
    x_homme = x_femme + 0.5
    homme_femme = np.concatenate((x_femme,x_homme))
    
    data_femme = [full_measures_young_femme.mean(), full_measures_mid_femme.mean(), full_measures_old_femme.mean()]
    data_homme = [full_measures_young_homme.mean(), full_measures_mid_homme.mean(), full_measures_old_homme.mean()]
    stderr_femme = [stderr_full_young_femme, stderr_full_mid_femme, stderr_full_old_femme]
    stderr_homme = [stderr_full_young_homme, stderr_full_mid_homme, stderr_full_old_homme]

    axs[0,0].bar(x_femme, data_femme, 0.08, label='Women', color='tab:red', yerr=stderr_femme, capsize=5)
    axs[0,0].bar(x_homme, data_homme, 0.08, label='Men', color='tab:blue', yerr=stderr_homme, capsize=5)
    
    axs[0,0].set_xticks(homme_femme)
    axs[0,0].set_xticklabels(categories * 2)
    axs[0,0].set_title(f"{name} - every phones")
    axs[0,0].set_ylabel(f"{name}")
    axs[0,0].set_xlabel("speakers")
    axs[0,0].grid()

    
    axs[0,1].bar(x_femme, [phoneme_a_measures_young_femme.mean(),phoneme_a_measures_mid_femme.mean(), phoneme_a_measures_old_femme.mean()], 0.08, label = "Femmes", color = "tab:red",yerr=[stderr_phoneme_a_young_femme,stderr_phoneme_a_mid_femme,stderr_phoneme_a_old_femme],capsize=5 )
    axs[0,1].bar(x_homme, [phoneme_a_measures_young_homme.mean(),phoneme_a_measures_mid_homme.mean(), phoneme_a_measures_old_homme.mean()], 0.08, label = "Hommes" , color = "tab:blue",yerr=[stderr_phoneme_a_young_homme,stderr_phoneme_a_mid_homme,stderr_phoneme_a_old_homme],capsize=5 )
    axs[0,1].set_xticks(homme_femme)
    axs[0,1].set_xticklabels(categories*2)
    axs[0,1].set_title(f"{name} - /a/")
    axs[0,1].set_ylabel(f"{name}")
    axs[0,1].set_xlabel("speakers")
    axs[0,1].grid()
    
    axs[1,0].bar(x_femme, [labial_a_measures_young_femme.mean(),labial_a_measures_mid_femme.mean(), labial_a_measures_old_femme.mean()], 0.08, label = "Femmes", color = "tab:red", yerr=[stderr_labial_a_young_femme,stderr_labial_a_mid_femme,stderr_labial_a_old_femme],capsize=5 )
    axs[1,0].bar(x_homme, [labial_a_measures_young_homme.mean(),labial_a_measures_mid_homme.mean(), labial_a_measures_old_homme.mean()], 0.08, label = "Hommes", color = "tab:blue", yerr=[stderr_labial_a_young_homme,stderr_labial_a_mid_homme,stderr_labial_a_old_homme],capsize=5 )
    axs[1,0].set_xticks(homme_femme) 
    axs[1,0].set_xticklabels(categories*2)
    axs[1,0].set_title(f"{name} - labial - /a/")
    axs[1,0].set_ylabel(f"{name}")
    axs[1,0].set_xlabel("speakers")
    axs[1,0].grid()
    
    axs[1,1].bar(x_femme, [a_pause_measures_young_femme.mean(),a_pause_measures_mid_femme.mean(), a_pause_measures_old_femme.mean()], 0.08, label = "Femmes", color = "tab:red",yerr=[stderr_a_pause_young_femme,stderr_a_pause_mid_femme,stderr_a_pause_old_femme],capsize=5 )
    axs[1,1].bar(x_homme, [a_pause_measures_young_homme.mean(),a_pause_measures_mid_homme.mean(), a_pause_measures_old_homme.mean()], 0.08, label = "Hommes", color = "tab:blue", yerr=[stderr_a_pause_young_homme,stderr_a_pause_mid_homme,stderr_a_pause_old_homme],capsize=5 )
    axs[1,1].set_xticks(homme_femme) 
    axs[1,1].set_xticklabels(categories*2)
    axs[1,1].set_title(f"{name} - /a/ - pause")
    axs[1,1].set_ylabel(f"{name}")
    axs[1,1].set_xlabel("speakers")
    axs[1,1].grid()
    
############################################################################
    
    
    handles, labels = axs[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, 0))

    plt.suptitle(f"{name} average by sexe and age category", fontsize=20, y=1.02)
    plt.tight_layout(rect=[0, 0.05, 1, 1])  
    #plt.savefig(f"bar_results/{descriptor}.png")
    plt.show()
    
descriptors = ["CPP", "harmonicity", "COG", "f0", "spectral_tilt"]
for descriptor in descriptors :
    make_plot(descriptor)