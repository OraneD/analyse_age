#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 21:12:40 2023

@author: orane
"""

import polars as pl
import matplotlib.pyplot as plt
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

def extract_s_meancog_meanskew(df,phoneme):

    #filtes rows where 'phoneme' is 's'
    s_phonemes_df = df.filter(pl.col("phoneme") == phoneme)
    print(s_phonemes_df)
    s_phonemes_df.write_csv("s_values_all_corpus.csv")

    #group by 'locuteur' and calculate the mean of 'cog' and 'skew', also taking the first 'age' (assuming it's always the same age for 1 loc)
    grouped_df = s_phonemes_df.group_by("locuteur").agg([
        pl.col("age").first().alias("age"),
        pl.col("sexe").first().alias("sexe"),
        pl.col("cog").mean().alias("mean_cog"),
        pl.col("skew").mean().alias("mean_skew")
        ])
    print(grouped_df)
    #converts the resulting DataFrame to a dictionary
    locuteur_dict = grouped_df.to_dict(as_series=False)

    #Reformat the dictionary to the desired structure
    result_dict = {locuteur_dict['locuteur'][i]: (locuteur_dict['age'][i], locuteur_dict["sexe"][i], locuteur_dict['mean_cog'][i], locuteur_dict['mean_skew'][i]) for i in range(len(locuteur_dict['locuteur']))}
    return(result_dict)

phoneme = "s"
s_values_per_loc = extract_s_meancog_meanskew(whole_dataframe,phoneme)



values = [v for v in s_values_per_loc.values()]
a = [(values[i][2], values[i][3]) for i in range(len(values))]

x = [x[0] for x in a]
y = [y[1] for y in a]
plt.figure(figsize=(15,7))
for i in range(len(x)):
    if values[i][0] < 35:
        marker = "v"
    elif 35 <= values[i][0] <= 60:
        marker = "o"
    else:
        marker = ","
    color= "blue" if values[i][1] == "homme" else "red"
    plt.scatter(x[i], 
                y[i],
                marker=marker,
                color=color,
                s=50
                )
    
###### Legend ############
plt.scatter([], [], color = "red", marker="v", label = "Femme - Age < 35")
plt.scatter([], [], color = "red", marker="o", label = "Femme - Age 35-60")
plt.scatter([], [], color = "red", marker=",", label = "Femme - Age > 60")
plt.scatter([], [], color = "blue", marker="v", label = "Homme - Age < 35")
plt.scatter([], [], color = "blue", marker="o", label = "Homme - Age 35-60")
plt.scatter([], [], color = "blue", marker=",", label = "Homme - Age > 60")

plt.legend()
plt.grid()
plt.xlabel("Average COG")
plt.ylabel("Average Skewness")
plt.title(f"Average Skweness and COG variations of /{phoneme}/ by age and gender")
plt.show()


