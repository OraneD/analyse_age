#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:09:56 2024

@author: orane
"""

import pandas as pd 
import glob

files = glob.glob("loc_modulation/*/*.csv")

big_df = pd.DataFrame()
for file in files :
    df_file = pd.read_csv(file)
    big_df = pd.concat([big_df,df_file])

big_df.to_csv("cepstral_modulation_full_df.csv")