#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:29:09 2024

@author: orane
"""

import pandas as pd
import csv

def load_csv(metadonnees):
    with open(metadonnees, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
        return(data)
    
data = load_csv("result_test.csv")

uniq_fichier = set([line["fichier"] for line in data])

with open("test_result_percentage.csv", "w") as file :
    file.write("fichier,age,reponse_jeune,reponse_vieux,nb_reponses,pourcentage_jeune,pourcentage_vieux\n")
    
    for fichier in sorted(uniq_fichier) :
        total_reponse_1 = 0
        total_reponse = 0
        total_reponse_2 = 0
        for line in data :
            fichier_data = line["fichier"]
            reponse = line["reponse"]
            
            if int(reponse) == 3 :
                continue
            if fichier_data == fichier :
                reponse = line["reponse"]
                age_loc = line["age_locuteur"]
                nb_reponses = line["nb_reponses"]
                total_reponse += int(nb_reponses)
                if int(reponse) == 2 :
                    total_reponse_2 += int(nb_reponses)
                elif int(reponse) == 1 :
                    total_reponse_1 += int(nb_reponses)
        percentage_1 = total_reponse_1 / total_reponse * 100
        percentage_1 = round(percentage_1,2)
        percentage_2 = total_reponse_2 / total_reponse * 100
        percentage_2 = round(percentage_2,2)
        file.write(f"{fichier},{age_loc},{total_reponse_1},{total_reponse_2},{total_reponse},{percentage_1},{percentage_2}\n")


            
            
    