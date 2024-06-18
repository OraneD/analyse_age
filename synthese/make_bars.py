#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:26:53 2024

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

    
def make_plot(descriptor,model_results):
    name = get_descriptor_name(descriptor)
    
#####################################################################################################################
####################################FEMMES###########################################################################
    
    full_df_old_femme, full_df_young_femme = get_age_cat(full_df)
    full_measures_old_femme = full_df_old_femme[descriptor].dropna()
    full_measures_young_femme = full_df_young_femme[descriptor].dropna()
    stderr_full_young_femme = full_measures_young_femme.std() / np.sqrt(len(full_measures_young_femme))
    stderr_full_old_femme = full_measures_old_femme.std() / np.sqrt(len(full_measures_old_femme))
    
#####################################################################################################################
######################################################################################################################
    fig,ax = plt.subplots(figsize=(10, 12))
    
    categories = ["<30", ">60"]
    x_femme = np.arange(len(categories))
    
    data_femme = [full_measures_young_femme.mean(), full_measures_old_femme.mean()]
    stderr_femme = [stderr_full_young_femme, stderr_full_old_femme]

    ax.bar(x_femme, data_femme, 0.4, label='Women', color='tab:red', yerr=stderr_femme, capsize=5)
    ax.set_xticks(x_femme)
    ax.set_xticklabels(categories)
    ax.set_ylabel(f"{name}")
    ax.set_xlabel("locuteurs")
    plt.grid()

    model_info = f"Intercept (<30): Coef={model_results['Intercept'][0]:.3f}, Std.Err={model_results['Intercept'][1]:.3f} (z={model_results['Intercept'][2]:.2f}, p={model_results['Intercept'][3]:.3f}\n"
    model_info += f">60: Coef={model_results['age_cat[T.old]'][0]:.3f}, Stdr.Err={model_results['age_cat[T.old]'][1]:.3f}, z={model_results['age_cat[T.old]'][2]:.3f}, p={model_results['age_cat[T.old]'][3]:.3f}"
    plt.figtext(0.5, 0.01, f"Résultats du modèle mixte pour {name}:", ha='center', va='top', fontsize=14, color='black')
    plt.figtext(0.5, -0.04, model_info, ha='center', va='top', fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":10}, usetex=False)
    plt.tight_layout()
    plt.savefig(f"plots/{descriptor}.png",bbox_inches='tight')
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
    
   
    return results

    
descriptors = ["CPP", "harmonicity", "COG", "f0", "spectral_tilt"]
for descriptor in descriptors :
    
    model_result = mixed_model(full_df,descriptor)
    make_plot(descriptor,model_result)