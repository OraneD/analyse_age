#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 17:37:02 2024

@author: orane
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

df = pd.read_csv('predictions_trainAll_testAll.csv')
df["duree_moy_segment"] = df["duree_moy_segment"] * 1000

def add_prediction_accuracy(df):
    conditions_correct = (
        ((df['age'] == 'old') & (df['pred_old'] > df['pred_young'])) |
        ((df['age'] == 'young') & (df['pred_young'] > df['pred_old']))
    )
    df['prediction_accuracy'] = conditions_correct.astype(int)
    return df

df = add_prediction_accuracy(df)
df["locuteur"] = [x.split("_")[2] for x in list(df["fichier"])]


df_femme_old = df[(df["sexe"] == "femme") & (df["age"] == "old")]
df_femme_young = df[(df["sexe"] == "femme") & (df["age"] == "young")]
df_homme_old = df[(df["sexe"] == "homme") & (df["age"] == "old")]
df_homme_young = df[(df["sexe"] == "homme") & (df["age"] == "young")]

descriptors = [ "duree_moy_segment", "moy_F0_voyelles", "articulation_rate", "pente"]

def fit_mixed_model(df, descriptor):
    df = df.dropna(subset=[descriptor])
    model = smf.mixedlm(f"{descriptor} ~ prediction_accuracy", df, groups=df["locuteur"])
    result = model.fit()
    print(f"Results for {descriptor}")
    print(result.summary())
    
    mean_incorrect = result.params['Intercept']
    mean_correct = result.params['Intercept'] + result.params['prediction_accuracy']
    
    print(f"Moyenne ajustée pour les prédictions incorrectes : {mean_incorrect}")
    print(f"Moyenne ajustée pour les prédictions correctes : {mean_correct}")
    
    return result

results = {
    'femmes_old': {}, 'femmes_young': {}, 
    'hommes_old': {}, 'hommes_young': {}
}

for descriptor in descriptors:
    print(f"Mixed Model Results for {descriptor} - Femmes Agées")
    results['femmes_old'][descriptor] = fit_mixed_model(df_femme_old, descriptor)
    print("\n" + "="*80 + "\n")
    
    print(f"Mixed Model Results for {descriptor} - Femmes Jeunes")
    results['femmes_young'][descriptor] = fit_mixed_model(df_femme_young, descriptor)
    print("\n" + "="*80 + "\n")
    
    print(f"Mixed Model Results for {descriptor} - Hommes Agés")
    results['hommes_old'][descriptor] = fit_mixed_model(df_homme_old, descriptor)
    print("\n" + "="*80 + "\n")
    
    print(f"Mixed Model Results for {descriptor} - Hommes Jeunes")
    results['hommes_young'][descriptor] = fit_mixed_model(df_homme_young, descriptor)
    print("\n" + "="*80 + "\n")
