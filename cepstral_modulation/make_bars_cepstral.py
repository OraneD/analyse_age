#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 18:02:28 2024

@author: orane
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("cepstral_modulation_full_df.csv")

df_femme = df[df["sexe"]=="femme"]
df_homme = df[df["sexe"]=="homme"]

def get_age_cat_df(df):
    young = df[df["age_cat"]=="young"]
    mid = df[df["age_cat"] =="mid"]
    old = df[df["age_cat"] == "old"]
    return young, mid, old

femme_young, femme_mid, femme_old = get_age_cat_df(df_femme)
homme_young, homme_mid, homme_old = get_age_cat_df(df_homme)

femme_young_mean = femme_young["mean_supmedian_Peaks"].dropna().mean()
femme_mid_mean = femme_mid["mean_supmedian_Peaks"].dropna().mean()
femme_old_mean = femme_old["mean_supmedian_Peaks"].dropna().mean()

homme_young_mean = homme_young["mean_supmedian_Peaks"].dropna().mean()
homme_mid_mean = homme_mid["mean_supmedian_Peaks"].dropna().mean()
homme_old_mean = homme_old["mean_supmedian_Peaks"].dropna().mean()

femme_young_std = femme_young["mean_supmedian_Peaks"].dropna().std() / np.sqrt(len(femme_young["mean_supmedian_Peaks"].dropna()))
femme_mid_std = femme_mid["mean_supmedian_Peaks"].dropna().std() / np.sqrt(len(femme_mid["mean_supmedian_Peaks"].dropna()))
femme_old_std = femme_old["mean_supmedian_Peaks"].dropna().std() / np.sqrt(len(femme_old["mean_supmedian_Peaks"].dropna()))

homme_young_std = homme_young["mean_supmedian_Peaks"].dropna().std() / np.sqrt(len(homme_young["mean_supmedian_Peaks"].dropna()))
homme_mid_std = homme_mid["mean_supmedian_Peaks"].dropna().std() / np.sqrt(len(homme_mid["mean_supmedian_Peaks"].dropna()))
homme_old_std = homme_old["mean_supmedian_Peaks"].dropna().std() / np.sqrt(len(homme_old["mean_supmedian_Peaks"].dropna()))

fig, ax = plt.subplots(figsize=(10,7))
categories = ["<30", "30-60", ">60"]
x_femme = np.arange(len(categories)) * 0.1
x_homme = x_femme + 0.5
homme_femme = np.concatenate((x_femme,x_homme))

ax.bar(x_femme, [femme_young_mean,femme_mid_mean,femme_old_mean], 0.08, yerr=[femme_young_std,femme_mid_std,femme_old_std], color="tab:red", label="femmes", capsize=5)
ax.bar(x_homme, [homme_young_mean,homme_mid_mean,homme_old_mean], 0.08, yerr=[homme_young_std,homme_mid_std,homme_old_std], color="tab:blue", label="hommes", capsize=5)
ax.set_xticks(homme_femme)
ax.set_xticklabels(categories*2)
ax.set_ylabel("Moyenne des pics supérieurs à la médiane")
ax.set_xlabel("locuteurs")
ax.grid()
plt.legend()
plt.show()
