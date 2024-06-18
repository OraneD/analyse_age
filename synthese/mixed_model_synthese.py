#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 18:44:08 2024

@author: orane
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

full_df = pd.read_csv("ESLO2_synthesis_acoustic_measures.csv")



def mixed_model(df_evaluated, descriptor):
    df_evaluated = df_evaluated.dropna(subset=[descriptor, "classe_age", "fichier"])
    model = smf.mixedlm(f"{descriptor} ~ classe_age", df_evaluated, groups=df_evaluated["fichier"])
    mdf = model.fit()
    print()
    print(f"{descriptor}")
    print(f"formule = {descriptor} ~ classe_age + 1|locuteur")
    print()
    print(mdf.summary())
    print()
    
mixed_model(full_df, "CPP")
