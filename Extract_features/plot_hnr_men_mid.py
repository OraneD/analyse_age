#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 17:16:15 2024

@author: orane
"""
import pandas as pd
import matplotlib.pyplot as plt

full_df = pd.read_csv("ESLO2_acoustic_measures_all.csv")


def get_by_sexe(df, sexe):
    return df[df["sexe"] == sexe]

full_df_homme = get_by_sexe(full_df,"homme")
def plot_raucite_boxplot_by_speaker(df):
    mid = df[df["classe_age"] == "mid"]
    unique_speakers = mid['locuteur'].unique()
    unique_speakers_name = [x.split("_")[-1] for x in unique_speakers]
    data = []
    for speaker in unique_speakers:
        speaker_data = df[df['locuteur'] == speaker]

        data.append(speaker_data['harmonicity'].dropna())
        
    fig, ax = plt.subplots(figsize=(15, 8))
    bp = ax.boxplot(data, labels=unique_speakers_name)

    ax.set_title('HNR par Locuteur - Hommes 30>=60')
    ax.set_xlabel('Locuteur')
    ax.set_ylabel('HNR')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
plot_raucite_boxplot_by_speaker(full_df_homme)






def plot_hnr_with_median(df):
    mid = df[df["classe_age"] == "mid"]
    young = df[df["classe_age"] == "young"]
    old = df[df["classe_age"] == "old"]

    unique_speakers = mid['locuteur']. unique()
    unique_speakers_name = [x.split("_")[-1] for x in unique_speakers]

    data = [mid[mid['locuteur'] == speaker]['harmonicity'].dropna() for speaker in unique_speakers]

    young_median = young['harmonicity'].median()
    old_median = old['harmonicity'].median()

    fig, ax = plt.subplots(figsize=(15, 12))
    bp = ax.boxplot(data, labels=unique_speakers_name, patch_artist=True)
    box_color = 'lightblue'
    for patch in bp['boxes']:
       patch.set_facecolor(box_color)
    for median in bp['medians']:
        median.set_color('black')
        median.set_linewidth(2)

    ax.axhline(y=young_median, color='r', linestyle='--', label='<30 Médiane', lw=3)
    ax.axhline(y=old_median, color='g', linestyle='--', label='>60 Médiane', lw=3)

    ax.set_title('HNR par Locuteur - Hommes 30>=60')
    ax.set_xlabel('Locuteur')
    ax.set_ylabel('HNR')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    plt.show()

plot_hnr_with_median(full_df_homme)
