#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:21:58 2024

@author: orane
"""
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
import matplotlib.patches as mpatches
import pandas as pd
import matplotlib.pyplot as plt
from make_mean_df import concat_df_per_cat



df_femme = concat_df_per_cat("femme")
df_homme = concat_df_per_cat("homme")
opensmile_features = [
   'pcm_fftMag_fband250-650', 'pcm_fftMag_fband1000-4000',
   'pcm_fftMag_spectralRollOff25.0', 'pcm_fftMag_spectralRollOff50.0',
   'pcm_fftMag_spectralRollOff75.0', 'pcm_fftMag_spectralRollOff90.0',
   'pcm_fftMag_spectralFlux', 'pcm_fftMag_spectralCentroid',
   'pcm_fftMag_spectralEntropy', 'pcm_fftMag_spectralVariance',
   'pcm_fftMag_spectralSkewness', 'pcm_fftMag_spectralKurtosis',
   'pcm_fftMag_spectralSlope', 'pcm_fftMag_psySharpness',
   'pcm_fftMag_spectralHarmonicity'
]
def rescale_data(df) :
    X = df.iloc[:, 2:]
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    df.iloc[:, 2:] = X_scaled
    df.to_csv("test_rescale.csv")
    return df

def make_vectors(df):
    X_pivot = df.pivot_table(index=['locuteur', 'age', 'sexe'], columns='phonemes', values=opensmile_features)
    X_pivot.columns = [f'{measure}_{phoneme}' for measure, phoneme in X_pivot.columns]
    X_reset = X_pivot.reset_index()
    X_reset.to_csv("test.csv")
    X = X_reset.drop(columns=['locuteur', 'age', 'sexe'])
    y = X_reset['age']
    imputer = SimpleImputer(strategy='mean')
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    X = rescale_data(X)
    return y, X



def reduce_TSNE(data, age) :
    tsne = TSNE(n_components=2, random_state=42)
    tsne_results = tsne.fit_transform(data)
    df_tsne = pd.DataFrame(tsne_results, columns=['TSNE1', 'TSNE2'])
    df_tsne["age"] = age
    return df_tsne

def choose_color(age) :
    if age == "mid" :
        return "green"
    elif age == "old" :
        return "red"
    elif age == "young":
        return "blue"
    
def visualise(dataframe_femme, dataframe_homme) :
    fig, axs = plt.subplots(1,2, figsize=(15,7))
    i = 0
    while i < len(dataframe_femme["TSNE1"]) :
        color = choose_color(list(dataframe_femme["age"])[i])
        axs[0].scatter(list(dataframe_femme["TSNE1"])[i], list(dataframe_femme["TSNE2"])[i], color = color)
        i += 1
    axs[0].set_title("Femmes")
    axs[0].set_xlabel('TSNE1')
    axs[0].set_ylabel('TSNE2')
    axs[0].legend()
    axs[0].grid()
    
    j = 0
    while j < len(dataframe_homme["TSNE1"]) :
        color = choose_color(list(dataframe_homme["age"])[j])
        axs[1].scatter(list(dataframe_homme["TSNE1"])[j], list(dataframe_homme["TSNE2"])[j], color = color)
        j += 1
    axs[1].set_title("Hommes")
    axs[1].set_xlabel('TSNE1')
    axs[1].set_ylabel('TSNE2')
    axs[1].legend()
    axs[1].grid()
    
    
    legend_elements = [mpatches.Patch(color='blue', label='Young'),
                   mpatches.Patch(color='green', label='Mid'),
                   mpatches.Patch(color='red', label='Old')]
    axs[0].legend(handles=legend_elements, title="Catégories")
    axs[1].legend(handles=legend_elements, title="Catégories")

    

    plt.suptitle("T-SNE réduction sur les valeurs moyennes de chaque phonème")
    plt.tight_layout()
    plt.show()
        
    

def main():
    y_femme, X_femme = make_vectors(df_femme)
    df_tsne_femme = reduce_TSNE(X_femme, y_femme)
    y_homme, X_homme = make_vectors(df_homme)
    df_tsne_homme = reduce_TSNE(X_homme, y_homme)
    visualise(df_tsne_femme, df_tsne_homme)
    
if __name__ == "__main__" :
    main()
    
