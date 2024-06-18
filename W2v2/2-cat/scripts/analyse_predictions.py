#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 01:06:02 2024

@author: orane
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


df = pd.read_csv('predictions_trainAll_testAll.csv')
df["duree_moy_segment"] = df["duree_moy_segment"] * 1000


############################## Femmes ##############################################
df_femme = df[df["sexe"] == "femme"]

df_correct_preds_femme = df_femme[((df_femme['age'] == 'old') & (df_femme['pred_old'] > df_femme['pred_young'])) |
                      ((df_femme['age'] == 'young') & (df_femme['pred_young'] > df_femme['pred_old']))]
df_old_femme = df_correct_preds_femme[df_correct_preds_femme['age'] == 'old'].dropna()
df_young_femme = df_correct_preds_femme[df_correct_preds_femme['age'] == 'young'].dropna()

df_incorrect_preds_femme = df_femme[((df_femme['age'] == 'old') & (df_femme['pred_old'] < df_femme['pred_young'])) |
                      ((df_femme['age'] == 'young') & (df_femme['pred_young'] < df_femme['pred_old']))]
df_old_incorrect_femme = df_incorrect_preds_femme[df_incorrect_preds_femme['age'] == 'old'].dropna()
df_young_incorrect_femme = df_incorrect_preds_femme[df_incorrect_preds_femme['age'] == 'young'].dropna()

############################# Hommes #################################################
df_homme = df[df["sexe"] == "homme"]

df_correct_preds_homme = df_homme[((df_homme['age'] == 'old') & (df_homme['pred_old'] > df_homme['pred_young'])) |
                                  ((df_homme['age'] == 'young') & (df_homme['pred_young'] > df_homme['pred_old']))]
df_old_homme = df_correct_preds_homme[df_correct_preds_homme['age'] == 'old'].dropna()
df_young_homme = df_correct_preds_homme[df_correct_preds_homme['age'] == 'young'].dropna()

df_incorrect_preds_homme = df_homme[((df_homme['age'] == 'old') & (df_homme['pred_old'] < df_homme['pred_young'])) |
                                    ((df_homme['age'] == 'young') & (df_homme['pred_young'] < df_homme['pred_old']))]
df_old_incorrect_homme = df_incorrect_preds_homme[df_incorrect_preds_homme['age'] == 'old'].dropna()
df_young_incorrect_homme = df_incorrect_preds_homme[df_incorrect_preds_homme['age'] == 'young'].dropna()

############################# Hommes #################################################

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
        
    data_femme = [df_old_femme[descriptor], df_young_femme[descriptor], df_old_incorrect_femme[descriptor], df_young_incorrect_femme[descriptor]]
    data_homme = [df_old_homme[descriptor], df_young_homme[descriptor], df_old_incorrect_homme[descriptor], df_young_incorrect_homme[descriptor]]
    
    labels = ['>60 bien prédit', '<30 bien prédit ', ">60 mal prédit", "<30 mal prédit"]
    
    colors = ['green', 'green', 'red', 'red']
    
    for i, data in enumerate(data_femme):
        box = axs[0].boxplot(data, positions=[i], patch_artist=True, showfliers=False, widths=0.3)
        for patch in box['boxes']:
            patch.set_facecolor(colors[i])
        for element in ['whiskers', 'caps', 'medians']:
                plt.setp(box[element], color='black')

    
    axs[0].set_title(f"{name} - Femmes")
    axs[0].set_ylabel(f"{name}")
    axs[0].set_xticks(range(len(labels)))
    axs[0].set_xticklabels(labels)
    axs[0].set_xlabel("séquences")
    
    for i, data in enumerate(data_homme):
        box = axs[1].boxplot(data, positions=[i], patch_artist=True, showfliers=False, widths=0.3)
        for patch in box['boxes']:
            patch.set_facecolor(colors[i])
            for element in ['whiskers', 'caps', 'medians']:
                plt.setp(box[element], color='black')

    
    axs[1].set_title(f"{name} - Hommes")
    axs[1].set_ylabel(f"{name}")
    axs[1].set_xticks(range(len(labels)))
    axs[1].set_xticklabels(labels)
    axs[1].set_xlabel("séquences")
    
    plt.tight_layout()
    plt.show()
    
def add_prediction_accuracy(df):
    conditions_correct = (
        ((df['age'] == 'old') & (df['pred_old'] > df['pred_young'])) |
        ((df['age'] == 'young') & (df['pred_young'] > df['pred_old']))
    )
    df['prediction_accuracy'] = conditions_correct.astype(int)
    return df

df = add_prediction_accuracy(df)

df["locuteur"] = [x.split("_")[2] for x in list(df["fichier"])]

df_femme = df[df["sexe"] == "femme"]
df_homme = df[df["sexe"] == "homme"]
print(df["prediction_accuracy"])

descriptors = ["duree", "duree_moy_segment", "moy_F0_voyelles", "articulation_rate", "pente"]

def fit_mixed_model(df, descriptor):
    model = smf.mixedlm(f"{descriptor} ~ prediction_accuracy * age", df, groups=df["locuteur"])    
    result = model.fit()
    print(result.summary())
    return result

for descriptor in descriptors:
    print(f"Mixed Model Results for {descriptor} - Femmes")
    fit_mixed_model(df_femme, descriptor)
    print("\n" + "="*80 + "\n")
    
    print(f"Mixed Model Results for {descriptor} - Hommes")
    fit_mixed_model(df_homme, descriptor)
    print("\n" + "="*80 + "\n")
