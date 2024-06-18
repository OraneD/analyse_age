#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:48:03 2024

@author: odufour
"""

from get_train import get_metadata_per_sexe, load_metadata, get_full_corpus_vector

metadata = load_metadata()
metadata_femme = get_metadata_per_sexe(metadata, "femme")
X, y, all_filenames = get_full_corpus_vector(metadata_femme)
print(f"Final size for train - X : {X.shape}, y : {y.shape}")

