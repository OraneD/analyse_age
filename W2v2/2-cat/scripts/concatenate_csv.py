#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 00:25:33 2024

@author: orane
"""

import pandas as pd
import os


csv_principal_path = 'corpus_description.csv'  
dossier_predictions_path = 'predictions/'  

df_principal = pd.read_csv(csv_principal_path)


predictions = pd.DataFrame()

for fichier in os.listdir(dossier_predictions_path):
    if fichier.endswith('.csv'):
        chemin_complet = os.path.join(dossier_predictions_path, fichier)
        df_temp = pd.read_csv(chemin_complet)
        predictions = pd.concat([predictions, df_temp], ignore_index=True)

predictions.rename(columns={'Filename': 'fichier'}, inplace=True)
predictions['fichier'] = predictions['fichier'].str.replace('.wav', '', regex=False)

print(predictions)
df_principal = pd.merge(df_principal, predictions, on='fichier', how='left')
df_principal.to_csv('predictions.csv', index=False)
