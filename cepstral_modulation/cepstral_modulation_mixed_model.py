#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 10:13:25 2024

@author: odufour
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

full_df = pd.read_csv("cepstral_modulation_full_df.csv")
def get_by_sexe(df, sexe):
    return df[df["sexe"] == sexe]

full_df_femme = get_by_sexe(full_df, "femme")
full_df_homme = get_by_sexe(full_df, "homme")


def mixed_model(df_evaluated, descriptor, sexe):
    df_evaluated = df_evaluated.dropna(subset=[descriptor, "age_cat", "locuteur"])
    model = smf.mixedlm(f"{descriptor} ~ age_cat ", df_evaluated, groups=df_evaluated["locuteur"])
    mdf = model.fit()
    print()
    print(f"{descriptor} sexe : {sexe}")
    print(f"formule = {descriptor} ~ classe_age + 1|locuteur")
    print()
    print(mdf.summary())
    print()
    
mixed_model(full_df_femme, "mean_supmedian_Peaks", "femme")
mixed_model(full_df_homme, "mean_supmedian_Peaks", "homme")

#mixed_model(full_df_femme, "mean_positiv_Peaks", "femme")
#mixed_model(full_df_homme, "mean_positiv_Peaks", "homme")


#mixed_model(full_df_femme, "mean_SpectralChange", "femme")
#mixed_model(full_df_homme, "mean_SpectralChange", "homme")



