#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:48:35 2024

@author: orane
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

full_df = pd.read_csv("ESLO2_acoustic_measures_all.csv")


def get_by_sexe(df, sexe):
    return df[df["sexe"] == sexe]

full_df_femme = get_by_sexe(full_df, "femme")
full_df_homme = get_by_sexe(full_df, "homme")

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


def mixed_model(df_evaluated, descriptor, sexe):
    df_evaluated = df_evaluated.dropna(subset=[descriptor, "classe_age", "locuteur"])
    model = smf.mixedlm(f"{descriptor} ~ C(classe_age, Treatment('mid'))", df_evaluated, groups=df_evaluated["locuteur"])
    mdf = model.fit()
    print()
    print(f"{descriptor} sexe : {sexe}")
    print(f"formule = {descriptor} ~ classe_age + 1|locuteur")
    print()
    print(mdf.summary())
    print()
    random_effects = mdf.random_effects
    fixed_effect = mdf.fe_params["Intercept"]
    fixed_effect_old = mdf.fe_params.get("C(classe_age, Treatment('mid'))[T.old]", 0)
    fixed_effect_young = mdf.fe_params.get("C(classe_age, Treatment('mid'))[T.young]", 0)

    random_effects_df = pd.DataFrame.from_dict(random_effects, orient='index')
    random_effects_df.columns = ['Random Effect']
    random_effects_df.reset_index(inplace=True)
    random_effects_df.rename(columns={'index': 'Locuteur'}, inplace=True)

    random_effects_df = random_effects_df.merge(df_evaluated[['locuteur', 'classe_age']].drop_duplicates(), left_on='Locuteur', right_on='locuteur')
    age_colors = {'young': 'red', 'mid': 'orange', 'old': 'blue'}
    random_effects_df['Color'] = random_effects_df['classe_age'].map(age_colors)
        
    descriptor_name = get_descriptor_name(descriptor)
    age_order = {'young': 1, 'mid': 2, 'old': 3}
    random_effects_df['age_order'] = random_effects_df['classe_age'].map(age_order)
    random_effects_df.sort_values(by=['age_order', 'Locuteur'], inplace=True)
    
    plt.figure(figsize=(16, 12))
    
    plt.subplot(2, 1, 1)
    plt.bar(random_effects_df['Locuteur'], random_effects_df['Random Effect'], color=random_effects_df['Color'])
    plt.xlabel(f'Locuteurs ({sexe})')
    plt.ylabel('Effet Aléatoire')
    plt.title(f'Effets Aléatoires par Locuteur pour {descriptor_name}, effet fixe = {fixed_effect}')
    plt.xticks(rotation=90)
    plt.grid(True)
    
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in age_colors.values()]
    labels = ["<30", "30>=60", ">60"]
    plt.legend(handles, labels)
    
    plt.subplot(2, 1, 2)
    adjusted_values = fixed_effect + random_effects_df['Random Effect']
    adjusted_values += random_effects_df['classe_age'].map({'young': fixed_effect_young, 'mid': 0, 'old': fixed_effect_old})
    
    bars = plt.bar(random_effects_df['Locuteur'], adjusted_values, color=random_effects_df['Color'], label='Valeur ajustée')
    
    for bar, re in zip(bars, random_effects_df['Random Effect']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{re:.2f}', ha='center', va='bottom')

    plt.axhline(y=fixed_effect, color='black', linestyle='--', label=f'Intercept (30>=60): {fixed_effect:.2f}', alpha = 0.5)

    plt.xlabel('Locuteurs')
    plt.xticks(rotation=90)
    plt.ylabel(f'{descriptor_name} Ajusté')
    plt.title(f'{descriptor_name} Ajusté pour tous les locuteurs')
    plt.legend(handles=[plt.Line2D([0], [0], color='black', linestyle='--', lw=2)], labels=[f'Intercept (30>=60): {fixed_effect:.2f}'])
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"{descriptor}_random_effect_{sexe}.png")
    plt.show()
    
    significant_effects = random_effects_df[np.abs(random_effects_df['Random Effect'].dropna()) > 0.2 * np.abs(fixed_effect)]
    
    print(f"Resultats pour {sexe} \n")
    

descriptors = ["CPP", "harmonicity", "COG", "f0", "spectral_tilt"]

for descriptor in descriptors : 
    mixed_model(full_df_femme, descriptor, "femme")
    mixed_model(full_df_homme, descriptor, "homme")







