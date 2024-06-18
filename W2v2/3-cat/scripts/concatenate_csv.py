#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 00:25:33 2024

@author: orane
"""

import pandas as pd
import os
import glob


csv_principal_path = 'corpus_description_mid.csv'  
dossier_predictions_path = 'predictions/*_weighted.csv'
df_principal = pd.read_csv(csv_principal_path)


predictions = pd.DataFrame()

for fichier in glob.glob(dossier_predictions_path):
    if fichier.endswith('.csv'):
        df_temp = pd.read_csv(fichier)
        print(df_temp)
        predictions = pd.concat([predictions, df_temp], ignore_index=True)


predictions.rename(columns={'Filename': 'fichier'}, inplace=True)
predictions['fichier'] = predictions['fichier'].str.replace('.wav', '', regex=False)

print(predictions)
df_principal = pd.merge(df_principal, predictions, on='fichier', how='left')
df_principal.to_csv('predictions.csv', index=False)
