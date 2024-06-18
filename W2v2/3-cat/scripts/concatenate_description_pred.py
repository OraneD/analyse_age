#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 14:55:15 2024

@author: orane
"""

import pandas as pd


df_femme = pd.read_csv("pred_12loc_femme.csv")
df_homme = pd.read_csv("pred_12loc_homme.csv")
df2 = pd.concat([df_femme, df_homme], ignore_index=True)


df1 = pd.read_csv("description_loc_corpus.csv")
df2['Filename'] = df2['Filename'].str.replace('.wav', '', regex=False)
merged_df = df1.merge(df2, left_on='fichier', right_on='Filename', how='left')
merged_df.drop('Filename', axis=1, inplace=True)
merged_df.to_csv("merged.csv", index=False)
