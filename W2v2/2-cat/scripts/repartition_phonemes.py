#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 14:11:09 2024

@author: orane
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



df = pd.read_csv('predictions_trainAll_testAll.csv')
df_femme = df[df["sexe"] == "femme"]
df_homme = df[df["sexe"] == "homme"]

femme_bad_predictions_young = df_femme[((df_femme['age'] == 'young') & (df_femme['pred_young'] < df_femme['pred_old']))]
femme_good_predictions_young = df_femme[((df_femme['age'] == 'young') & (df_femme['pred_young'] > df_femme['pred_old']))]
femme_bad_predictions_old = df_femme[((df_femme['age'] == 'old') & (df_femme['pred_young'] > df_femme['pred_old']))]
femme_good_predictions_old = df_femme[((df_femme['age'] == 'old') & (df_femme['pred_young'] < df_femme['pred_old']))]

homme_bad_predictions_young = df_homme[((df_homme['age'] == 'young') & (df_homme['pred_young'] < df_homme['pred_old']))]
homme_good_predictions_young = df_homme[((df_homme['age'] == 'young') & (df_homme['pred_young'] > df_homme['pred_old']))]
homme_bad_predictions_old = df_homme[((df_homme['age'] == 'old') & (df_homme['pred_young'] > df_homme['pred_old']))]
homme_good_predictions_old = df_homme[((df_homme['age'] == 'old') & (df_homme['pred_young'] < df_homme['pred_old']))]

###################### Phonèmes #########################################

femme_good_nb_pause_old = femme_good_predictions_old["nb_pause"].mean()
femme_good_nb_pause_young = femme_good_predictions_young["nb_pause"].mean()
femme_bad_nb_pause_old = femme_bad_predictions_old["nb_pause"].mean()
femme_bad_nb_pause_young = femme_bad_predictions_young["nb_pause"].mean()

femme_good_nb_voyelles_old = femme_good_predictions_old["nb_voyelle_orale"].mean()
femme_good_nb_voyelles_young = femme_good_predictions_young["nb_voyelle_orale"].mean()
femme_bad_nb_voyelles_old = femme_bad_predictions_old["nb_voyelle_orale"].mean()
femme_bad_nb_voyelles_young = femme_bad_predictions_young["nb_voyelle_orale"].mean()


femme_good_nb_nasales_old = femme_good_predictions_old["nb_voyelle_nasale"].mean()
femme_good_nb_nasales_young = femme_good_predictions_young["nb_voyelle_nasale"].mean()
femme_bad_nb_nasales_old = femme_bad_predictions_old["nb_voyelle_nasale"].mean()
femme_bad_nb_nasales_young = femme_bad_predictions_young["nb_voyelle_nasale"].mean()

femme_good_nb_occlusive_old = femme_good_predictions_old["nb_occlusive"].mean()
femme_good_nb_occlusive_young = femme_good_predictions_young["nb_occlusive"].mean()
femme_bad_nb_occlusive_old = femme_bad_predictions_old["nb_occlusive"].mean()
femme_bad_nb_occlusive_young = femme_bad_predictions_young["nb_occlusive"].mean()

femme_good_nb_sonante_old = femme_good_predictions_old["nb_sonante"].mean()
femme_good_nb_sonante_young = femme_good_predictions_young["nb_sonante"].mean()
femme_bad_nb_sonante_old = femme_bad_predictions_old["nb_sonante"].mean()
femme_bad_nb_sonante_young = femme_bad_predictions_young["nb_sonante"].mean()

femme_good_nb_fricative_old = femme_good_predictions_old["nb_fricative"].mean()
femme_good_nb_fricative_young = femme_good_predictions_young["nb_fricative"].mean()
femme_bad_nb_fricative_old = femme_bad_predictions_old["nb_fricative"].mean()
femme_bad_nb_fricative_young = femme_bad_predictions_young["nb_fricative"].mean()

femme_good_nb_consnasal_old = femme_good_predictions_old["nb_nasale"].mean()
femme_good_nb_consnasal_young = femme_good_predictions_young["nb_nasale"].mean()
femme_bad_nb_consnasal_old = femme_bad_predictions_old["nb_nasale"].mean()
femme_bad_nb_consnasal_young = femme_bad_predictions_young["nb_nasale"].mean()

good_predictions_means = [
    femme_good_nb_pause_old, femme_good_nb_pause_young,
    femme_good_nb_voyelles_old, femme_good_nb_voyelles_young,
    femme_good_nb_nasales_old, femme_good_nb_nasales_young,
    femme_good_nb_occlusive_old, femme_good_nb_occlusive_young,
    femme_good_nb_sonante_old, femme_good_nb_sonante_young,
    femme_good_nb_fricative_old, femme_good_nb_fricative_young,
    femme_good_nb_consnasal_old, femme_good_nb_consnasal_young
]

bad_predictions_means = [
    femme_bad_nb_pause_old, femme_bad_nb_pause_young,
    femme_bad_nb_voyelles_old, femme_bad_nb_voyelles_young,
    femme_bad_nb_nasales_old, femme_bad_nb_nasales_young,
    femme_bad_nb_occlusive_old, femme_bad_nb_occlusive_young,
    femme_bad_nb_sonante_old, femme_bad_nb_sonante_young,
    femme_bad_nb_fricative_old, femme_bad_nb_fricative_young,
    femme_bad_nb_consnasal_old, femme_bad_nb_consnasal_young
]

homme_good_nb_pause_old = homme_good_predictions_old["nb_pause"].mean()
homme_good_nb_pause_young = homme_good_predictions_young["nb_pause"].mean()
homme_bad_nb_pause_old = homme_bad_predictions_old["nb_pause"].mean()
homme_bad_nb_pause_young = homme_bad_predictions_young["nb_pause"].mean()

homme_good_nb_voyelles_old = homme_good_predictions_old["nb_voyelle_orale"].mean()
homme_good_nb_voyelles_young = homme_good_predictions_young["nb_voyelle_orale"].mean()
homme_bad_nb_voyelles_old = homme_bad_predictions_old["nb_voyelle_orale"].mean()
homme_bad_nb_voyelles_young = homme_bad_predictions_young["nb_voyelle_orale"].mean()

homme_good_nb_nasales_old = homme_good_predictions_old["nb_voyelle_nasale"].mean()
homme_good_nb_nasales_young = homme_good_predictions_young["nb_voyelle_nasale"].mean()
homme_bad_nb_nasales_old = homme_bad_predictions_old["nb_voyelle_nasale"].mean()
homme_bad_nb_nasales_young = homme_bad_predictions_young["nb_voyelle_nasale"].mean()

homme_good_nb_occlusive_old = homme_good_predictions_old["nb_occlusive"].mean()
homme_good_nb_occlusive_young = homme_good_predictions_young["nb_occlusive"].mean()
homme_bad_nb_occlusive_old = homme_bad_predictions_old["nb_occlusive"].mean()
homme_bad_nb_occlusive_young = homme_bad_predictions_young["nb_occlusive"].mean()

homme_good_nb_sonante_old = homme_good_predictions_old["nb_sonante"].mean()
homme_good_nb_sonante_young = homme_good_predictions_young["nb_sonante"].mean()
homme_bad_nb_sonante_old = homme_bad_predictions_old["nb_sonante"].mean()
homme_bad_nb_sonante_young = homme_bad_predictions_young["nb_sonante"].mean()

homme_good_nb_fricative_old = homme_good_predictions_old["nb_fricative"].mean()
homme_good_nb_fricative_young = homme_good_predictions_young["nb_fricative"].mean()
homme_bad_nb_fricative_old = homme_bad_predictions_old["nb_fricative"].mean()
homme_bad_nb_fricative_young = homme_bad_predictions_young["nb_fricative"].mean()

homme_good_nb_consnasal_old = homme_good_predictions_old["nb_nasale"].mean()
homme_good_nb_consnasal_young = homme_good_predictions_young["nb_nasale"].mean()
homme_bad_nb_consnasal_old = homme_bad_predictions_old["nb_nasale"].mean()
homme_bad_nb_consnasal_young = homme_bad_predictions_young["nb_nasale"].mean()

homme_good_predictions_means = [
    homme_good_nb_pause_old, homme_good_nb_pause_young,
    homme_good_nb_voyelles_old, homme_good_nb_voyelles_young,
    homme_good_nb_nasales_old, homme_good_nb_nasales_young,
    homme_good_nb_occlusive_old, homme_good_nb_occlusive_young,
    homme_good_nb_sonante_old, homme_good_nb_sonante_young,
    homme_good_nb_fricative_old, homme_good_nb_fricative_young,
    homme_good_nb_consnasal_old, homme_good_nb_consnasal_young
]

homme_bad_predictions_means = [
    homme_bad_nb_pause_old, homme_bad_nb_pause_young,
    homme_bad_nb_voyelles_old, homme_bad_nb_voyelles_young,
    homme_bad_nb_nasales_old, homme_bad_nb_nasales_young,
    homme_bad_nb_occlusive_old, homme_bad_nb_occlusive_young,
    homme_bad_nb_sonante_old, homme_bad_nb_sonante_young,
    homme_bad_nb_fricative_old, homme_bad_nb_fricative_young,
    homme_bad_nb_consnasal_old, homme_bad_nb_consnasal_young
]

######################CALCUL DES POURCENTAGES#################################
homme_total_phonemes_old = homme_good_predictions_old[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
homme_total_phonemes_young = homme_good_predictions_young[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
homme_total_phonemes_old_bad = homme_bad_predictions_old[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
homme_total_phonemes_young_bad = homme_bad_predictions_young[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()

homme_good_pct_consnasal_old = (homme_good_nb_consnasal_old / homme_total_phonemes_old) * 100
homme_good_pct_consnasal_young = (homme_good_nb_consnasal_young / homme_total_phonemes_young) * 100
homme_bad_pct_consnasal_old = (homme_bad_nb_consnasal_old / homme_total_phonemes_old_bad) * 100
homme_bad_pct_consnasal_young = (homme_bad_nb_consnasal_young / homme_total_phonemes_young_bad) * 100

homme_good_pct_nb_pause_old = (homme_good_nb_pause_old / homme_total_phonemes_old) * 100
homme_good_pct_nb_pause_young = (homme_good_nb_pause_young / homme_total_phonemes_young) * 100
homme_bad_pct_nb_pause_old = (homme_bad_nb_pause_old / homme_total_phonemes_old_bad) * 100
homme_bad_pct_nb_pause_young = (homme_bad_nb_pause_young / homme_total_phonemes_young_bad) * 100

homme_good_pct_nb_voyelles_old = (homme_good_nb_voyelles_old / homme_total_phonemes_old) * 100
homme_good_pct_nb_voyelles_young = (homme_good_nb_voyelles_young / homme_total_phonemes_young) * 100
homme_bad_pct_nb_voyelles_old = (homme_bad_nb_voyelles_old / homme_total_phonemes_old_bad) * 100
homme_bad_pct_nb_voyelles_young = (homme_bad_nb_voyelles_young / homme_total_phonemes_young_bad) * 100

homme_good_pct_nb_fricatives_old = (homme_good_nb_fricative_old / homme_total_phonemes_old) * 100
homme_good_pct_nb_fricatives_young = (homme_good_nb_fricative_young / homme_total_phonemes_young) * 100
homme_bad_pct_nb_fricatives_old = (homme_bad_nb_fricative_old / homme_total_phonemes_old_bad) * 100
homme_bad_pct_nb_fricatives_young = (homme_bad_nb_fricative_young / homme_total_phonemes_young_bad) * 100

homme_good_pct_nb_occlusive_old = (homme_good_nb_occlusive_old / homme_total_phonemes_old) * 100
homme_good_pct_nb_occlusive_young = (homme_good_nb_occlusive_young / homme_total_phonemes_young) * 100
homme_bad_pct_nb_occlusive_old = (homme_bad_nb_occlusive_old / homme_total_phonemes_old_bad) * 100
homme_bad_pct_nb_occlusive_young = (homme_bad_nb_occlusive_young / homme_total_phonemes_young_bad) * 100

homme_good_pct_nb_sonantes_old = (homme_good_nb_sonante_old / homme_total_phonemes_old) * 100
homme_good_pct_nb_sonantes_young = (homme_good_nb_sonante_young / homme_total_phonemes_young) * 100
homme_bad_pct_nb_sonantes_old = (homme_bad_nb_sonante_old / homme_total_phonemes_old_bad) * 100
homme_bad_pct_nb_sonantes_young = (homme_bad_nb_sonante_young / homme_total_phonemes_young_bad) * 100

homme_good_pct_nb_nasales_old = (homme_good_nb_nasales_old / homme_total_phonemes_old) * 100
homme_good_pct_nb_nasales_young = (homme_good_nb_nasales_young / homme_total_phonemes_young) * 100
homme_bad_pct_nb_nasales_old = (homme_bad_nb_nasales_old / homme_total_phonemes_old_bad) * 100
homme_bad_pct_nb_nasales_young = (homme_bad_nb_nasales_young / homme_total_phonemes_young_bad) * 100

homme_good_pct_means = [
    homme_good_pct_nb_pause_old, homme_good_pct_nb_pause_young,
    homme_good_pct_nb_voyelles_old, homme_good_pct_nb_voyelles_young,
    homme_good_pct_nb_nasales_old, homme_good_pct_nb_nasales_young,
    homme_good_pct_nb_occlusive_old, homme_good_pct_nb_occlusive_young,
    homme_good_pct_nb_sonantes_old, homme_good_pct_nb_sonantes_young,
    homme_good_pct_nb_fricatives_old, homme_good_pct_nb_fricatives_young,
    homme_good_pct_consnasal_old, homme_good_pct_consnasal_young
]
homme_bad_pct_means = [
    homme_bad_pct_nb_pause_old, homme_bad_pct_nb_pause_young,
    homme_bad_pct_nb_voyelles_old, homme_bad_pct_nb_voyelles_young,
    homme_bad_pct_nb_nasales_old, homme_bad_pct_nb_nasales_young,
    homme_bad_pct_nb_occlusive_old, homme_bad_pct_nb_occlusive_young,
    homme_bad_pct_nb_sonantes_old, homme_bad_pct_nb_sonantes_young,
    homme_bad_pct_nb_fricatives_old, homme_bad_pct_nb_fricatives_young,
    homme_bad_pct_consnasal_old, homme_bad_pct_consnasal_young
]

femme_total_phonemes_old = femme_good_predictions_old[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
femme_total_phonemes_young = femme_good_predictions_young[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
femme_total_phonemes_old_bad = femme_bad_predictions_old[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()
femme_total_phonemes_young_bad = femme_bad_predictions_young[['nb_nasale', 'nb_occlusive', 'nb_sonante', 'nb_fricative', 'nb_semi-voyelle', "nb_pause", "nb_voyelle_orale", "nb_voyelle_nasale"]].sum(axis=1).mean()

femme_good_pct_consnasal_old = (femme_good_nb_consnasal_old / femme_total_phonemes_old) * 100
femme_good_pct_consnasal_young = (femme_good_nb_consnasal_young / femme_total_phonemes_young) * 100
femme_bad_pct_consnasal_old = (femme_bad_nb_consnasal_old / femme_total_phonemes_old_bad) * 100
femme_bad_pct_consnasal_young = (femme_bad_nb_consnasal_young / femme_total_phonemes_young_bad) * 100

femme_good_pct_nb_pause_old = (femme_good_nb_pause_old / femme_total_phonemes_old) * 100
femme_good_pct_nb_pause_young = (femme_good_nb_pause_young / femme_total_phonemes_young) * 100
femme_bad_pct_nb_pause_old = (femme_bad_nb_pause_old / femme_total_phonemes_old_bad) * 100
femme_bad_pct_nb_pause_young = (femme_bad_nb_pause_young / femme_total_phonemes_young_bad) * 100

femme_good_pct_nb_voyelles_old = (femme_good_nb_voyelles_old / femme_total_phonemes_old) * 100
femme_good_pct_nb_voyelles_young = (femme_good_nb_voyelles_young / femme_total_phonemes_young) * 100
femme_bad_pct_nb_voyelles_old = (femme_bad_nb_voyelles_old / femme_total_phonemes_old_bad) * 100
femme_bad_pct_nb_voyelles_young = (femme_bad_nb_voyelles_young / femme_total_phonemes_young_bad) * 100

femme_good_pct_nb_fricatives_old = (femme_good_nb_fricative_old / femme_total_phonemes_old) * 100
femme_good_pct_nb_fricatives_young = (femme_good_nb_fricative_young / femme_total_phonemes_young) * 100
femme_bad_pct_nb_fricatives_old = (femme_bad_nb_fricative_old / femme_total_phonemes_old_bad) * 100
femme_bad_pct_nb_fricatives_young = (femme_bad_nb_fricative_young / femme_total_phonemes_young_bad) * 100

femme_good_pct_nb_occlusive_old = (femme_good_nb_occlusive_old / femme_total_phonemes_old) * 100
femme_good_pct_nb_occlusive_young = (femme_good_nb_occlusive_young / femme_total_phonemes_young) * 100
femme_bad_pct_nb_occlusive_old = (femme_bad_nb_occlusive_old / femme_total_phonemes_old_bad) * 100
femme_bad_pct_nb_occlusive_young = (femme_bad_nb_occlusive_young / femme_total_phonemes_young_bad) * 100

femme_good_pct_nb_sonantes_old = (femme_good_nb_sonante_old / femme_total_phonemes_old) * 100
femme_good_pct_nb_sonantes_young = (femme_good_nb_sonante_young / femme_total_phonemes_young) * 100
femme_bad_pct_nb_sonantes_old = (femme_bad_nb_sonante_old / femme_total_phonemes_old_bad) * 100
femme_bad_pct_nb_sonantes_young = (femme_bad_nb_sonante_young / femme_total_phonemes_young_bad) * 100

femme_good_pct_nb_nasales_old = (femme_good_nb_nasales_old / femme_total_phonemes_old) * 100
femme_good_pct_nb_nasales_young = (femme_good_nb_nasales_young / femme_total_phonemes_young) * 100
femme_bad_pct_nb_nasales_old = (femme_bad_nb_nasales_old / femme_total_phonemes_old_bad) * 100
femme_bad_pct_nb_nasales_young = (femme_bad_nb_nasales_young / femme_total_phonemes_young_bad) * 100

femme_good_pct_means = [
    femme_good_pct_nb_pause_old, femme_good_pct_nb_pause_young,
    femme_good_pct_nb_voyelles_old, femme_good_pct_nb_voyelles_young,
    femme_good_pct_nb_nasales_old, femme_good_pct_nb_nasales_young,
    femme_good_pct_nb_occlusive_old, femme_good_pct_nb_occlusive_young,
    femme_good_pct_nb_sonantes_old, femme_good_pct_nb_sonantes_young,
    femme_good_pct_nb_fricatives_old, femme_good_pct_nb_fricatives_young,
    femme_good_pct_consnasal_old, femme_good_pct_consnasal_young
]
femme_bad_pct_means = [
    femme_bad_pct_nb_pause_old, femme_bad_pct_nb_pause_young,
    femme_bad_pct_nb_voyelles_old, femme_bad_pct_nb_voyelles_young,
    femme_bad_pct_nb_nasales_old, femme_bad_pct_nb_nasales_young,
    femme_bad_pct_nb_occlusive_old, femme_bad_pct_nb_occlusive_young,
    femme_bad_pct_nb_sonantes_old, femme_bad_pct_nb_sonantes_young,
    femme_bad_pct_nb_fricatives_old, femme_bad_pct_nb_fricatives_young,
    femme_bad_pct_consnasal_old, femme_bad_pct_consnasal_young
]

################################Visualisation##########################################


categories = ['Pause', 'Voyelles', 'Voy-Nasales', 'Occlusives', 'Sonantes', 'Fricative', 'Cons-Nasales']
x = np.arange(len(categories))  
bar_width = 0.35
offset = bar_width / 2  

fig, axs = plt.subplots(2, 2, figsize=(12, 10), sharey="row")

axs[0, 0].bar(x - offset, good_predictions_means[::2], bar_width, label='Bonnes prédictions - >60', color='tab:green', edgecolor="white")
axs[0, 0].bar(x + offset, good_predictions_means[1::2], bar_width, label='Bonnes prédictions - <30', color='green', edgecolor="white")
axs[0, 0].set_title('Bonnes prédictions - Femmes')
axs[0, 0].set_xticks(x)
axs[0, 0].set_ylim(0,8)
axs[0, 0].set_xticklabels(categories, rotation=45)
axs[0, 0].set_ylabel('Nombre moyen')
axs[0, 0].legend()

axs[0, 1].bar(x - offset, bad_predictions_means[::2], bar_width, label='Mauvaises prédictions - >60', color='tab:red', edgecolor='white')
axs[0, 1].bar(x + offset, bad_predictions_means[1::2], bar_width, label='Mauvaises prédictions - <30', color='red', edgecolor='white')
axs[0, 1].set_title('Mauvaises prédictions - Femmes')
axs[0, 1].set_xticks(x)
axs[0, 1].set_xticklabels(categories, rotation=45)
axs[0, 1].set_ylabel('Nombre moyen')
axs[0, 1].legend()

axs[1, 0].bar(x - offset, homme_good_predictions_means[::2], bar_width, label='Bonnes prédictions - >60', color='tab:green', edgecolor="white")
axs[1, 0].bar(x + offset, homme_good_predictions_means[1::2], bar_width, label='Bonnes prédictions - <30', color='green', edgecolor="white")
axs[1, 0].set_title('Bonnes prédictions - Hommes')
axs[1, 0].set_xticks(x)
axs[1, 0].set_ylim(0,8)
axs[1, 0].set_xticklabels(categories, rotation=45)
axs[1, 0].set_ylabel('Nombre moyen')
axs[1, 0].legend()

axs[1, 1].bar(x - offset, homme_bad_predictions_means[::2], bar_width, label='Mauvaises prédictions - >60', color='tab:red', edgecolor='white')
axs[1, 1].bar(x + offset, homme_bad_predictions_means[1::2], bar_width, label='Mauvaises prédictions - <30', color='red', edgecolor='white')
axs[1, 1].set_title('Mauvaises prédictions - Hommes')
axs[1, 1].set_xticks(x)
axs[1, 1].set_xticklabels(categories, rotation=45)
axs[1, 1].set_ylabel('Nombre moyen')
axs[1, 1].legend()

plt.tight_layout()
plt.show()
#################################### Pourcentages ########################################
categories = ['Pause', 'Voyelles', 'Voy-Nasales', 'Occlusives', 'Sonantes', 'Fricative', 'Cons-Nasales']
x = np.arange(len(categories))  
bar_width = 0.35  
offset = bar_width / 2  

fig, axs = plt.subplots(2, 2, figsize=(12, 10), sharey="row")

axs[0, 0].bar(x - offset, femme_good_pct_means[::2], bar_width, label='Bonnes prédictions - >60', color='green', edgecolor="white")
axs[0, 0].bar(x + offset, femme_good_pct_means[1::2], bar_width, label='Bonnes prédictions - <30', color='tab:green', edgecolor="white")
axs[0, 0].set_title('Bonnes predictions - Femmes')
axs[0, 0].set_xticks(x)
axs[0, 0].set_ylim(0,50)
axs[0, 0].set_xticklabels(categories, rotation=45)
axs[0, 0].set_ylabel('Proportion (%)')
axs[0, 0].legend()

axs[0, 1].bar(x - offset,femme_bad_pct_means[::2], bar_width, label='Mauvaises prédictions - >60', color='tab:red', edgecolor='white')
axs[0, 1].bar(x + offset, femme_bad_pct_means[1::2], bar_width, label='Mauvaises predictions - <30', color='red', edgecolor='white')
axs[0, 1].set_title('Mauvaises prédictions - Femmes')
axs[0, 1].set_xticks(x)
axs[0, 1].set_xticklabels(categories, rotation=45)
axs[0, 1].set_ylabel('Proportion (%)')
axs[0, 1].legend()

axs[1, 0].bar(x - offset, homme_good_pct_means[::2], bar_width, label='Bonnes prédictions - >60', color='green', edgecolor="white")
axs[1, 0].bar(x + offset, homme_good_pct_means[1::2], bar_width, label='Bonnes prédictions - <30', color='tab:green', edgecolor="white")
axs[1, 0].set_title('Bonnes prédictions - Hommes')
axs[1, 0].set_xticks(x)
axs[1, 0].set_xticklabels(categories, rotation=45)
axs[1, 0].set_ylabel('Proportion (%)')
axs[1, 0].legend()

axs[1, 1].bar(x - offset, homme_bad_pct_means[::2], bar_width, label='Mauvaises prédictions - >60', color='tab:red', edgecolor='white')
axs[1, 1].bar(x + offset, homme_bad_pct_means[1::2], bar_width, label='Mauvaises prédictions - <30', color='red', edgecolor='white')
axs[1, 1].set_title('Mauvaises prédictions - Hommes')
axs[1, 1].set_xticks(x)
axs[1, 0].set_ylim(0,50)
axs[1, 1].set_xticklabels(categories, rotation=45)
axs[1, 1].set_ylabel('Proportion (%)')
axs[1, 1].legend()

#plt.suptitle("Phonetic types proportions in good and bad predictions", fontsize=20, y=1.02)
plt.tight_layout()



categories = ['Pause', 'Voyelles', 'Voy-Nasales', 'Occlusives', 'Sonantes', 'Fricative', 'Cons-Nasales']
x = np.arange(len(categories))
bar_width = 0.35
offset = bar_width / 2



categories = ['Pause', 'Voyelles', 'Voy-Nasales', 'Occlusives', 'Sonantes', 'Fricative', 'Cons-Nasales']
x = np.arange(len(categories))
bar_width = 0.35
offset = bar_width / 2


good_pct_means_over_60 = [np.random.rand() * 50 for _ in range(len(categories))]
good_pct_means_under_30 = [np.random.rand() * 50 for _ in range(len(categories))]
bad_pct_means_over_60 = [np.random.rand() * 50 for _ in range(len(categories))]
bad_pct_means_under_30 = [np.random.rand() * 50 for _ in range(len(categories))]

fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)  # Deux groupes d'âge

axs[0].bar(x - offset, femme_good_pct_means, bar_width, label='Good Predictions', color='tab:green', edgecolor="white")
axs[0].bar(x + offset, femme_bad_pct_means, bar_width, label='Bad Predictions', color='tab:red', edgecolor="white")
axs[0].set_title('Women')
axs[0].set_xticks(x)
axs[0].set_xticklabels(categories, rotation=45)
axs[0].set_ylabel('Proportion (%)')
axs[0].legend()

axs[1].bar(x - offset, good_pct_means_under_30, bar_width, label='Good Predictions', color='tab:green', edgecolor="white")
axs[1].bar(x + offset, bad_pct_means_under_30, bar_width, label='Bad Predictions', color='tab:red', edgecolor="white")
axs[1].set_title('Men')
axs[1].set_xticks(x)
axs[1].set_xticklabels(categories, rotation=45)
axs[1].set_ylabel('Proportion (%)')
axs[1].legend()

plt.suptitle("Phonetic types proportions in good and bad predictions by age group", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()





