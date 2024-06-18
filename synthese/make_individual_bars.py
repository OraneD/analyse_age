#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:28:18 2024

@author: orane
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


full_df = pd.read_csv("ESLO2_synthesis_acoustic_measures.csv")

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

def make_plot(descriptor, model_results, median_young_color='grey', median_old_color='black'):
    name = get_descriptor_name(descriptor)
    
    full_df_old_femme, full_df_young_femme = get_age_cat(full_df)
    full_df_old_femme = full_df_old_femme[["fichier", descriptor]].dropna()
    full_df_young_femme = full_df_young_femme[["fichier", descriptor]].dropna()
    
    old_means = full_df_old_femme.groupby("fichier")[descriptor].mean()
    young_means = full_df_young_femme.groupby("fichier")[descriptor].mean()
    
    old_stderr = full_df_old_femme.groupby("fichier")[descriptor].std() / np.sqrt(full_df_old_femme.groupby("fichier")[descriptor].count())
    young_stderr = full_df_young_femme.groupby("fichier")[descriptor].std() / np.sqrt(full_df_young_femme.groupby("fichier")[descriptor].count())
    
    fig, ax = plt.subplots(figsize=(10, 12))
    
    all_means = pd.concat([young_means, old_means])
    all_stderr = pd.concat([young_stderr, old_stderr])
    colors = ['tab:red'] * len(young_means) + ['tab:orange'] * len(old_means)
    
    x = np.arange(len(all_means))
    
    ax.bar(x, all_means, 0.4, color=colors, yerr=all_stderr, capsize=5)
    
    ax.set_xticks(x)
    ax.set_xticklabels(all_means.index, rotation=90)
    ax.set_ylabel(f"{name}")
    ax.set_xlabel("locutrices")
    
    mean_young = full_df_young_femme[descriptor].mean()
    mean_old = full_df_old_femme[descriptor].mean()
    
    ax.axhline(mean_young, color=median_young_color, linestyle='--', label=f'Moyenne <30 ({mean_young:.2f})')
    ax.axhline(mean_old, color=median_old_color, linestyle='--', label=f'Moyenne >60 ({mean_old:.2f})')
    
    young_patch = plt.Line2D([0], [0], color='tab:red', lw=4, label='<60')
    old_patch = plt.Line2D([0], [0], color='tab:orange', lw=4, label='>60')
    
    handles, labels = ax.get_legend_handles_labels()
    handles.extend([young_patch, old_patch])
    
    plt.legend(handles=handles)
    plt.grid()
    
    model_info = f"Intercept (<30): Coef={model_results['Intercept'][0]:.3f}, Std.Err={model_results['Intercept'][1]:.3f} (z={model_results['Intercept'][2]:.2f}, p={model_results['Intercept'][3]:.3f}\n"
    model_info += f">60: Coef={model_results['age_cat[T.old]'][0]:.3f}, Stdr.Err={model_results['age_cat[T.old]'][1]:.3f}, z={model_results['age_cat[T.old]'][2]:.3f}, p={model_results['age_cat[T.old]'][3]:.3f}"
    
    plt.figtext(0.5, 0.01, f"Résultats du modèle mixte pour {name}:", ha='center', va='top', fontsize=14, color='black')
    plt.figtext(0.5, -0.04, model_info, ha='center', va='top', fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":10}, usetex=False)
    
    plt.tight_layout()
    plt.savefig(f"plots/{descriptor}.png", bbox_inches='tight')
    plt.show()

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
       
   random_effects = mdf.random_effects
   fixed_effect = mdf.fe_params["Intercept"]
   fixed_effect_old = mdf.fe_params.get("C(classe_age, Treatment('young'))[T.old]", 0)

   random_effects_df = pd.DataFrame.from_dict(random_effects, orient='index')
   random_effects_df.columns = ['Random Effect']
   random_effects_df.reset_index(inplace=True)
   random_effects_df.rename(columns={'index': 'Fichier'}, inplace=True)

   random_effects_df = random_effects_df.merge(df_evaluated[['fichier', 'classe_age']].drop_duplicates(), left_on='Fichier', right_on='fichier')
   
   age_colors = {'young': 'red', 'old': 'orange'}
   random_effects_df['Color'] = random_effects_df['classe_age'].map(age_colors)
   age_order = {'young': 1, 'old': 2}
   random_effects_df['age_order'] = random_effects_df['classe_age'].map(age_order)
   random_effects_df.sort_values(by=['age_order', 'Fichier'], inplace=True)
   descriptor_name = get_descriptor_name(descriptor)

   plt.figure(figsize=(12, 12))
   
   plt.subplot(2, 1, 1)
   plt.bar(random_effects_df['Fichier'], random_effects_df['Random Effect'], color=random_effects_df['Color'])
   plt.xlabel('Locuteurs')
   plt.ylabel('Effet Aléatoire')
   plt.title(f'Effets Aléatoires par Locuteur pour {descriptor_name}, effet fixe = {fixed_effect}')
   plt.xticks(rotation=90)
   plt.grid(True)
   
   handles = [plt.Line2D([0], [0], color=color, lw=4) for color in age_colors.values()]
   labels = ["<30", ">60"]
   plt.legend(handles, labels)
   
   plt.subplot(2, 1, 2)
   adjusted_values = fixed_effect + random_effects_df['Random Effect']
   adjusted_values += random_effects_df['classe_age'].map({'young': 0, 'old': fixed_effect_old})
   
   bars = plt.bar(random_effects_df['Fichier'], adjusted_values, color=random_effects_df['Color'])
   
   for bar, re in zip(bars, random_effects_df['Random Effect']):
       height = bar.get_height()
       plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{re:.2f}', ha='center', va='bottom')

   plt.axhline(y=fixed_effect, color='red', linestyle='--', label=f'Intercept <30: {fixed_effect:.2f}')

   plt.xlabel('Locuteurs')
   plt.ylabel(f'{descriptor_name} Ajusté')
   plt.title(f'{descriptor_name} Ajusté pour tous les locuteurs')
   plt.legend()
   plt.grid(True)

   plt.tight_layout()
   plt.savefig(f"{descriptor}_random_effect_synthese.png")
   plt.show()
   
   return results


descriptors = ["CPP", "harmonicity", "COG", "f0", "spectral_tilt"]
for descriptor in descriptors:
    model_result = mixed_model(full_df, descriptor)
    make_plot(descriptor, model_result, median_young_color='grey', median_old_color='black')
