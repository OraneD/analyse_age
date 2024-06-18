#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:35:10 2024

@author: orane
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cm_femmes = np.array([
    [118, 988, 3722],
    [37, 2982, 4643],
    [301, 3326, 9322]
])

cm_hommes = np.array([
    [576, 2155, 1098],
    [750, 7414, 327],
    [1967, 5511, 1737]
])

classes = ['<30', '>60', '30>=60']

def plot_confusion_matrix(ax, cm, classes, title):
    #sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes, ax=ax)
    sns.heatmap(cm, annot=True, fmt='.2f', cmap='Blues', xticklabels=classes, yticklabels=classes, ax=ax, cbar=False)
    ax.set_xlabel('Prédiction')
    ax.set_ylabel('Vrais étiquettes')
    ax.set_title(title)


fig, axes = plt.subplots(1, 2, figsize=(20, 7))

plot_confusion_matrix(axes[0], cm_femmes, classes, 'Matrice de Confusion - Femmes')
plot_confusion_matrix(axes[1], cm_hommes, classes, 'Matrice de Confusion - Hommes')

plt.tight_layout()
plt.show()

cm_femmes_normalized = cm_femmes.astype('float') / cm_femmes.sum(axis=1)[:, np.newaxis]
cm_hommes_normalized = cm_hommes.astype('float') / cm_hommes.sum(axis=1)[:, np.newaxis]
fig, axes = plt.subplots(1, 2, figsize=(20, 7))
plot_confusion_matrix(axes[0], cm_femmes_normalized, classes, 'Matrice de Confusion - Femmes')
plot_confusion_matrix(axes[1], cm_hommes_normalized, classes, 'Matrice de Confusion - Hommes')
plt.tight_layout()
plt.show()

