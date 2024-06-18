#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 11:58:36 2024

@author: orane
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('predictions_trainAll_testAll.csv')
df["duree_moy_segment"] = df["duree_moy_segment"] * 1000

df_1231 = df[df["fichier"].str.contains("ESLO2_ENTJEUN_1231")]
df_1075 = df[df["fichier"].str.contains("ESLO2_ENT_1075")]
loc_jeunes = df[df["age"] == "young"]
loc_vieux = df[df["age"] == "old"]
loc_jeunes_femmes = loc_jeunes[loc_jeunes["sexe"] == "femme"]
loc_jeunes_hommes = loc_jeunes[loc_jeunes["sexe"] == "homme"]
loc_vieux_femmes = loc_vieux[loc_vieux["sexe"] == "femme"]
loc_vieux_hommes = loc_vieux[loc_vieux["sexe"] == "homme"]


descriptors = ["duree", "duree_moy_segment", "moy_F0_voyelles", "articulation_rate", "pente"]


for descriptor in descriptors :
    fig, axs = plt.subplots(1,2, figsize=(16,7), sharey="row")
    if descriptor == "moy_F0_voyelles":
        name = "F0_voyelles"
    elif descriptor == "articulation_rate":
        name = "Débit (Phonèmes/secondes)"
    elif descriptor == "duree": 
        name = "Durée séquences (s)"
    elif descriptor == "duree_moy_segment" :
        name = "Durée moyenne segments (ms)"
    elif descriptor == "pente":
        name = "Pente (dB)"
        
    mean_jeune = loc_jeunes_femmes[f"{descriptor}"].dropna().mean()
    mean_vieux =loc_vieux_femmes[f"{descriptor}"].dropna().mean()
    mean_1231 = df_1231[f"{descriptor}"].dropna().mean()
    axs[0].axhline(mean_jeune, color="green", linestyle='--', label=f'Moyenne <30 ({mean_jeune:.2f})',alpha=0.5)
    axs[0].axhline(mean_vieux, color="black", linestyle='--', label=f'Moyenne >60 ({mean_vieux:.2f})',alpha=0.5)
    axs[0].axhline(mean_1231, color="red", linestyle='--', label=f'Moyenne 1231 ({mean_1231:.2f})',alpha=0.5)
    axs[0].boxplot([df_1231[f"{descriptor}"].dropna(), loc_jeunes_femmes[f"{descriptor}"].dropna(), loc_vieux_femmes[f"{descriptor}"].dropna()], labels=["ESLO2_ENTJEUN_1231", "Femmes < 30", "Femmes >60"], showfliers=False)
    #axs[0].set_title(f"1231")
    axs[0].set_ylabel(f"{name}")
    axs[0].set_xlabel("locuteurs")
    axs[0].legend()
    axs[0].grid()
    
    
    mean_jeune_hommes = loc_jeunes_hommes[f"{descriptor}"].dropna().mean()
    mean_vieux_hommes =loc_vieux_hommes[f"{descriptor}"].dropna().mean()
    mean_1075 = df_1075[f"{descriptor}"].dropna().mean()

    axs[1].axhline(mean_jeune_hommes, color="green", linestyle='--', label=f'Moyenne <30 ({mean_jeune_hommes:.2f})',alpha=0.5)
    axs[1].axhline(mean_vieux_hommes, color="black", linestyle='--', label=f'Moyenne >60 ({mean_vieux_hommes:.2f})',alpha=0.5)
    axs[1].axhline(mean_1231, color="blue", linestyle='--', label=f'Moyenne 1075 ({mean_1075:.2f})',alpha=0.5)

    axs[1].boxplot([df_1075[f"{descriptor}"].dropna(), loc_jeunes_hommes[f"{descriptor}"].dropna(), loc_vieux_hommes[f"{descriptor}"].dropna()], labels=["ESLO2_ENT_1075", "Hommes < 30", "Hommes >60"], showfliers=False)
    #axs[1].set_title(f"1075")
    axs[1].set_ylabel(f"{name}")
    axs[1].set_xlabel("locuteurs")
    axs[1].legend()
    axs[1].grid()
    plt.savefig(f"{descriptor}_comparison.png")

    plt.show()




