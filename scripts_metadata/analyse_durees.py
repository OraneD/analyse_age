#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 01:23:17 2023

@author: orane
"""

import polars as pl
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as mpatches


def load_dataframe(file):
    df = pl.read_csv(file, 
                     has_header=True,
                     infer_schema_length=100000
                     )
    #Converting "cog" and "skew" rows to float (they were string)
    df = df.with_columns([
    pl.col("cog").map_elements(lambda x: float(x) if x != "--undefined--" else float('nan')).alias("cog"),
    pl.col("skew").map_elements(lambda x: float(x) if x != "--undefined--" else float('nan')).alias("skew")
    ])
    return df

whole_dataframe=load_dataframe("../resultats_corpus_mfa_avec_md.csv")
print(whole_dataframe)

def extract_duree_vowels(df,vowels):

    s_phonemes_df = df.filter(pl.col("phoneme").is_in(vowels))

    grouped_df = s_phonemes_df.group_by("locuteur").agg([
        pl.col("age").first().alias("age"),
        pl.col("sexe").first().alias("sexe"),
        pl.col("duree").mean().alias("mean_duration"),
        ])
    print(grouped_df)

    locuteur_dict = grouped_df.to_dict(as_series=False)

    result_dict = {locuteur_dict['locuteur'][i]: (locuteur_dict['age'][i], locuteur_dict["sexe"][i], locuteur_dict['mean_duration'][i]) for i in range(len(locuteur_dict['locuteur']))}
    sorted_dict = dict(sorted(result_dict.items(), key=lambda item: item[1][0]))
    return sorted_dict

#vowels = ["o","i", "a", "e", "u", "y","ɔ","ɛ","ə","ø","ɑ̃","ɛ̃","œ̃","ɔ̃","œ"]
vowels = ["i"]
dict_vowels = extract_duree_vowels(whole_dataframe,vowels)


fig = plt.figure(figsize=(20,8))


ax = fig.add_axes([0,0,1,1])
values = [v for v in dict_vowels.values()]

for i, (age, sexe, duration) in enumerate(values):
    color = "tab:blue" if sexe == "homme" else "tab:orange"
    ax.bar(i, duration, color=color, width=0.4)

ax.set_xticks(range(len(values)))
ax.set_xticklabels([v[0] for v in values])
plt.ylabel("Durée moyenne des voyelles")
plt.xlabel("âge")
plt.title(f"Durée moyenne des voyelles par locuteur {vowels}")

plt.show()

