#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 00:28:51 2024

@author: orane
"""
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

full_df = pd.read_csv("ESLO2_synthesis_acoustic_measures.csv")

def normalize_data(series, invert=False):
    return 1 - (series - series.min()) / (series.max() - series.min())

def calculate_raucite_index(df):
    df['normalized_harmonicity'] = normalize_data(df['harmonicity'])
    df['normalized_spectral_tilt'] = normalize_data(df['spectral_tilt'])
    df['normalized_CPP'] = normalize_data(df['CPP'])

    poids_hnr = 0.1
    poids_slope = 0.1
    poids_cpp = 0.1

    df['Raucité'] = (df['normalized_harmonicity'].dropna() * poids_hnr + 
                     df['normalized_spectral_tilt'].dropna() * poids_slope + 
                     df['normalized_CPP'].dropna() * poids_cpp) / (poids_hnr + poids_slope + poids_cpp)
    return df

full_df = calculate_raucite_index(full_df)
print(full_df)

def plot_raucite_boxplot_by_speaker(df):
    unique_speakers = df['fichier'].unique()
    unique_speakers_name = [x.split("_")[-1] for x in unique_speakers]
    data = []
    colors = []

    for speaker in unique_speakers:
        speaker_data = df[df['fichier'] == speaker]
        data.append(speaker_data['Raucité'].dropna())
        age_color = 'tab:red' if (speaker_data['classe_age'].mode()[0] == 'young') else 'tab:orange'
        colors.append(age_color)

    fig, ax = plt.subplots(figsize=(15, 8))
    bp = ax.boxplot(data, patch_artist=True, labels=unique_speakers_name)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    for median in bp['medians']:
        median.set_color("black")
        median.set_linewidth(1)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='tab:red', label='<30'),
                       Patch(facecolor='tab:orange', label='>60')]
    ax.legend(handles=legend_elements)

    ax.set_title('Indice de Raucité par Locuteur - Corpus synthétisé')
    ax.set_xlabel('Locuteur')
    ax.set_ylabel('Indice de Raucité')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

plot_raucite_boxplot_by_speaker(full_df)

def plot_bar(df, model_results):
    full_young_femme = df[df["classe_age"]=="young"]
    full_measures_young_femme = full_young_femme["Raucité"]
    full_old_femme = df[df["classe_age"] == "old"]
    full_measures_old_femme = full_old_femme["Raucité"]
    stderr_full_young_femme = full_measures_young_femme.std() / np.sqrt(len(full_measures_young_femme))
    stderr_full_old_femme = full_measures_old_femme.std() / np.sqrt(len(full_measures_old_femme))

    fig,ax = plt.subplots(figsize=(10, 12))
    categories = ["<30", ">60"]
    x_femme = np.arange(len(categories))
    
    data_femme = [full_measures_young_femme.mean(), full_measures_old_femme.mean()]
    stderr_femme = [stderr_full_young_femme, stderr_full_old_femme]

    ax.bar(x_femme, data_femme, 0.4, label='Women', color='tab:red', yerr=stderr_femme, capsize=5)
    ax.set_xticks(x_femme)
    ax.set_xticklabels(categories)
    ax.set_ylabel(f"Indice de raucité")
    ax.set_xlabel("locuteurs")
    plt.grid()
    model_info = f"Intercept (<30): Coef={model_results['Intercept'][0]:.3f}, Std.Err={model_results['Intercept'][1]:.3f} (z={model_results['Intercept'][2]:.2f}, p={model_results['Intercept'][3]:.3f}\n"
    model_info += f">60: Coef={model_results['age_cat[T.old]'][0]:.3f}, Stdr.Err={model_results['age_cat[T.old]'][1]:.3f}, z={model_results['age_cat[T.old]'][2]:.3f}, p={model_results['age_cat[T.old]'][3]:.3f}"
    plt.figtext(0.5, 0.01, f"Résultats du modèle mixte pour l'indice de raucité :", ha='center', va='top', fontsize=14, color='black')
    plt.figtext(0.5, -0.04, model_info, ha='center', va='top', fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":10}, usetex=False)
    plt.tight_layout()
    

def mixed_model(df_evaluated, descriptor):
    df_evaluated = df_evaluated.dropna(subset=[descriptor, "classe_age", "fichier"])
    model = smf.mixedlm(f"{descriptor} ~ C(classe_age, Treatment('young'))", df_evaluated, groups=df_evaluated["fichier"])
    mdf = model.fit()
    print()
    print(f"{descriptor}")
    print(f"formule = {descriptor} ~ classe_age + 1|locuteur")
    print()
    print(mdf.summary())
    print()
    results = {
       'Intercept': (mdf.params['Intercept'], mdf.bse['Intercept'], mdf.tvalues['Intercept'], mdf.pvalues['Intercept'])}
    if 'C(classe_age, Treatment(\'young\'))[T.old]' in mdf.params:
        results['age_cat[T.old]'] = (
            mdf.params['C(classe_age, Treatment(\'young\'))[T.old]'], 
            mdf.bse['C(classe_age, Treatment(\'young\'))[T.old]'], 
            mdf.tvalues['C(classe_age, Treatment(\'young\'))[T.old]'], 
            mdf.pvalues['C(classe_age, Treatment(\'young\'))[T.old]']
        )
    
   
    return results
model_result = mixed_model(full_df,"Raucité")
plot_bar(full_df,model_result)

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

def plot_raucite_boxplot_by_speaker(ax, df):
    unique_speakers = df['fichier'].unique()
    unique_speakers_name = [x.split("_")[-1] for x in unique_speakers]
    data = []
    colors = []

    for speaker in unique_speakers:
        speaker_data = df[df['fichier'] == speaker]
        data.append(speaker_data['Raucité'].dropna())
        age_color = 'tab:red' if (speaker_data['classe_age'].mode()[0] == 'young') else 'tab:orange'
        colors.append(age_color)

    bp = ax.boxplot(data, patch_artist=True, labels=unique_speakers_name)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    for median in bp['medians']:
        median.set_color("black")
        median.set_linewidth(1)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='tab:red', label='<30'),
                       Patch(facecolor='tab:orange', label='>60')]
    ax.legend(handles=legend_elements)

    ax.set_title('Indice de Raucité par Locuteur - Corpus synthétisé')
    ax.set_xlabel('Locuteur')
    ax.set_ylabel('Indice de Raucité')
    ax.set_xticklabels(unique_speakers_name, rotation=45)
    ax.grid(True)

def plot_bar(ax, df, model_results):
    full_young_femme = df[df["classe_age"] == "young"]
    full_measures_young_femme = full_young_femme["Raucité"]
    full_old_femme = df[df["classe_age"] == "old"]
    full_measures_old_femme = full_old_femme["Raucité"]
    stderr_full_young_femme = full_measures_young_femme.std() / np.sqrt(len(full_measures_young_femme))
    stderr_full_old_femme = full_measures_old_femme.std() / np.sqrt(len(full_measures_old_femme))

    categories = ["<30", ">60"]
    x_femme = np.arange(len(categories))

    data_femme = [full_measures_young_femme.mean(), full_measures_old_femme.mean()]
    stderr_femme = [stderr_full_young_femme, stderr_full_old_femme]

    ax.bar(x_femme, data_femme, 0.4, label='Women', color='tab:red', yerr=stderr_femme, capsize=5)
    ax.set_xticks(x_femme)
    ax.set_xticklabels(categories)
    ax.set_ylabel("Indice de raucité")
    ax.set_xlabel("Locuteurs")
    ax.set_title("Indice de raucité moyen par catégorie d'âge")
    
    ax.grid(True)
    
    model_info = (f"Intercept (<30): Coef={model_results['Intercept'][0]:.3f}, Std.Err={model_results['Intercept'][1]:.3f} "
                  f"(z={model_results['Intercept'][2]:.2f}, p={model_results['Intercept'][3]:.3f})\n"
                  f">60: Coef={model_results['age_cat[T.old]'][0]:.3f}, Stdr.Err={model_results['age_cat[T.old]'][1]:.3f}, "
                  f"z={model_results['age_cat[T.old]'][2]:.3f}, p={model_results['age_cat[T.old]'][3]:.3f}")
    
    ax.text(-0.3, -0.1, f"Résultats du modèle mixte pour l'indice de raucité :\n{model_info}", 
            ha='center', va='top', fontsize=12, transform=ax.transAxes, bbox={"facecolor":"white", "alpha":0.5, "pad":10})

def mixed_model(df_evaluated, descriptor):
    df_evaluated = df_evaluated.dropna(subset=[descriptor, "classe_age", "fichier"])
    model = smf.mixedlm(f"{descriptor} ~ C(classe_age, Treatment('young'))", df_evaluated, groups=df_evaluated["fichier"])
    mdf = model.fit()
    print()
    print(f"{descriptor}")
    print(f"formule = {descriptor} ~ classe_age + 1|locuteur")
    print()
    print(mdf.summary())
    print()
    results = {
       'Intercept': (mdf.params['Intercept'], mdf.bse['Intercept'], mdf.tvalues['Intercept'], mdf.pvalues['Intercept'])
    }
    if 'C(classe_age, Treatment(\'young\'))[T.old]' in mdf.params:
        results['age_cat[T.old]'] = (
            mdf.params['C(classe_age, Treatment(\'young\'))[T.old]'], 
            mdf.bse['C(classe_age, Treatment(\'young\'))[T.old]'], 
            mdf.tvalues['C(classe_age, Treatment(\'young\'))[T.old]'], 
            mdf.pvalues['C(classe_age, Treatment(\'young\'))[T.old]']
        )
   
    return results

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 14))

plot_raucite_boxplot_by_speaker(axes[0], full_df)
model_result = mixed_model(full_df, "Raucité")
plot_bar(axes[1], full_df, model_result)

plt.tight_layout()
plt.show()
