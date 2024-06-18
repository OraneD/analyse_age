#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 00:14:17 2024

@author: orane
"""

import pandas as pd
from sklearn.metrics import classification_report
import numpy as np

df = pd.read_csv('predictions_trainAll_testAll.csv')  
df['predicted_label'] = np.where(df['pred_young'] > df['pred_old'], 'young', 'old')
report = classification_report(df['age'], df['predicted_label'], output_dict=True)
report_df = pd.DataFrame(report).transpose()
latex_table = report_df.to_latex(float_format="%.2f")
print(latex_table)
with open('classification_report.tex', 'w') as f:
    f.write(latex_table)
