#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 19:31:10 2024

@author: orane
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

df = pd.read_csv("predictions.csv")
print(df)


def is_misclassified(row):
    predictions = {'young': row['pred_young'], 'mid': row['pred_mid'], 'old': row['pred_old']}
    predicted_class = max(predictions, key=predictions.get)
    return predicted_class != row['classe_age']

def get_predicted_class(row):
    predictions = {'young': row['pred_young'], 'mid': row['pred_mid'], 'old': row['pred_old']}
    return max(predictions, key=predictions.get)

df['predicted'] = df.apply(get_predicted_class, axis=1)
df['misclassified'] = df.apply(is_misclassified, axis=1)
goodclassified_df = df[df["misclassified"] == False]
goodclassified_df['age_numeric'] = pd.to_numeric(goodclassified_df['age'], errors='coerce')
misclassified_df = df[df['misclassified']]
misclassified_df['age_numeric'] = pd.to_numeric(misclassified_df['age'], errors='coerce')
misclassified_counts = misclassified_df['classe_age'].value_counts()
misclassified_percentages = (misclassified_counts / misclassified_counts.sum()) * 100
print("-------Part de chaque classe dans les erreurs-----")
print(misclassified_percentages)
print("-------------------------------------")

predicted_distribution = {}
for actual_class in ['young', 'mid', 'old']:
    # Filter the misclassified dataframe for the current actual class
    class_df = misclassified_df[misclassified_df['classe_age'] == actual_class]
    # Calculate the percentage for each predicted class within the actual class
    predicted_distribution[actual_class] = class_df['predicted'].value_counts(normalize=True) * 100

print("Classes attribuées aux jeunes mal classés (%) :")
print(predicted_distribution["young"])
print("Classes attribuées aux mid mal classés (%) :")
print(predicted_distribution["mid"])
print("Classes attribuées aux vieux mal classés (%) :")
print(predicted_distribution["old"])


missclassified_old = misclassified_df[misclassified_df["classe_age"] == "old"]
missclassified_young = misclassified_df[misclassified_df["classe_age"] == "young"]
missclassified_mid = misclassified_df[misclassified_df["classe_age"] == "mid"]
goodclassified_old = goodclassified_df[goodclassified_df["classe_age"] == "old"]
goodclassified_young = goodclassified_df[goodclassified_df["classe_age"] == "young"]
goodclassified_mid = goodclassified_df[goodclassified_df["classe_age"] == "mid"]
print("Comparaison âge moyen des bien classés et mal classés")
print(f'âge moyen old mal classés : {missclassified_old["age_numeric"].mean()}, âge moyen vieux bien classés : {goodclassified_old["age_numeric"].mean()}')
print(f'âge moyen mid mal classés : {missclassified_mid["age_numeric"].mean()}, âge moyen mid bien classés : {goodclassified_mid["age_numeric"].mean()}')
print(f'âge moyen young mal classés : {missclassified_young["age_numeric"].mean()}, âge moyen young bien classés : {goodclassified_young["age_numeric"].mean()}')





