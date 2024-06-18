#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:10:37 2024

@author: orane
"""

import pandas as pd
import numpy as np

df = pd.read_csv('predictions_trainAll_testAll.csv')

df_femme = df[df["sexe"] == "femme"]
df_homme = df[df["sexe"] == "homme"]

femme_total_phonemes = df_femme[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
femme_good_total = df_femme[df_femme['pred_young'] > df_femme['pred_old']]
femme_bad_total = df_femme[df_femme['pred_young'] < df_femme['pred_old']]

homme_total_phonemes = df_homme[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
homme_good_total = df_homme[df_homme['pred_young'] > df_homme['pred_old']]
homme_bad_total = df_homme[df_homme['pred_young'] < df_homme['pred_old']]

def calc_percentages(df, total_phonemes):
    percentages = {}
    for col in ['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', 'nb_pause', 'nb_voyelle_orale', 'nb_voyelle_nasale']:
        percentages[col] = (df[col].mean() / total_phonemes) * 100
    return percentages

femme_good_pct = calc_percentages(femme_good_total, femme_total_phonemes)
femme_bad_pct = calc_percentages(femme_bad_total, femme_total_phonemes)
homme_good_pct = calc_percentages(homme_good_total, homme_total_phonemes)
homme_bad_pct = calc_percentages(homme_bad_total, homme_total_phonemes)

print("Femme Good Predictions Percentages:", femme_good_pct)
print("Femme Bad Predictions Percentages:", femme_bad_pct)
print("Homme Good Predictions Percentages:", homme_good_pct)
print("Homme Bad Predictions Percentages:", homme_bad_pct)

import matplotlib.pyplot as plt

categories = ['Nasale', 'Occlusive', 'Sonante', 'Fricative', 'Semi-voyelle', 'Pause', 'Voyelle Orale', 'Voyelle Nasale']
x = np.arange(len(categories))
bar_width = 0.35
offset = bar_width / 2

fig, axs = plt.subplots(1, 2, figsize=(12, 10), sharey=True)

axs[0].bar(x - offset, [femme_good_pct[col] for col in femme_good_pct], bar_width, label='Good Predictions', color='tab:green', edgecolor="white")
axs[0].bar(x + offset, [femme_bad_pct[col] for col in femme_bad_pct], bar_width, label='Bad Predictions', color='tab:red', edgecolor="white")
axs[0].set_title('Women')
axs[0].set_xticks(x)
axs[0].set_xticklabels(categories, rotation=45)
axs[0].set_ylabel('Proportion (%)')
axs[0].legend()
axs[0].grid()


axs[1].bar(x - offset, [homme_good_pct[col] for col in homme_good_pct], bar_width, label='Good Predictions', color='tab:green', edgecolor="white")
axs[1].bar(x + offset, [homme_bad_pct[col] for col in homme_bad_pct], bar_width, label='Bad Predictions', color='tab:red', edgecolor="white")
axs[1].set_title('Men')
axs[1].set_xticks(x)
axs[1].set_xticklabels(categories, rotation=45)
axs[1].set_ylabel('Proportion (%)')
axs[1].legend()
axs[1].grid()


plt.suptitle("Phonemics types proportions in good and bad predictions", fontsize=20, y=1.02)
plt.tight_layout()
plt.show()
