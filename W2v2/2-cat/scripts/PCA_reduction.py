#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 22:54:46 2024

@author: orane
"""

import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np

file_path = 'description_loc_corpus.csv'  
data = pd.read_csv(file_path)

data_femme = data[data["sexe"] == "femme"]
data_homme = data[data["sexe"] == "homme"]

data_young= data_femme[data_femme['age'] == 'young']  
data_old = data_femme[data_femme['age'] == 'old']

imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
data[data.columns[3:]] = imputer.fit_transform(data[data.columns[3:]])
features = data.columns[3:]  
x = data.loc[:, features].values


x = StandardScaler().fit_transform(x)


pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

finalDf = pd.concat([principalDf, data[['age']]], axis = 1) 

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

age_groups = ['young', 'old']
colors = ['r', 'g']
for age_group, color in zip(age_groups,colors):
    indicesToKeep = finalDf['age'] == age_group
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(age_groups)
ax.grid()

plt.show()
