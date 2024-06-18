#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:48:00 2024

@author: orane
"""

import csv
import pandas as pd
from scipy.stats import ttest_rel

    
data = pd.read_csv("test_result_percentage.csv")
data['type_voix'] = data['fichier'].apply(lambda x: 'lent' if 'lent' in x else 'normal')

grouped_data = data.groupby(['age', 'type_voix']).agg({
    'pourcentage_jeune': 'mean',
    'pourcentage_vieux': 'mean'
}).reset_index()

grouped_data['groupe_age'] = grouped_data['age'].apply(lambda x: 'jeune' if x < 30 else 'vieux')

average_data = grouped_data.groupby(['groupe_age', 'type_voix']).agg({
    'pourcentage_jeune': 'mean',
    'pourcentage_vieux': 'mean'
}).reset_index()

print(average_data)


data['groupe_age'] = data['age'].apply(lambda x: 'jeune' if x < 30 else 'vieux')

jeune_normal = data[(data['groupe_age'] == 'jeune') & (data['type_voix'] == 'normal')]['pourcentage_vieux']
jeune_lent = data[(data['groupe_age'] == 'jeune') & (data['type_voix'] == 'lent')]['pourcentage_vieux']

vieux_normal = data[(data['groupe_age'] == 'vieux') & (data['type_voix'] == 'normal')]['pourcentage_vieux']
vieux_lent = data[(data['groupe_age'] == 'vieux') & (data['type_voix'] == 'lent')]['pourcentage_vieux']

ttest_jeunes = ttest_rel(jeune_normal, jeune_lent)
ttest_vieux = ttest_rel(vieux_normal, vieux_lent)


print("T-test Jeunes : ")
print(ttest_jeunes)
print("T-test Vieux :")
print(ttest_vieux)
