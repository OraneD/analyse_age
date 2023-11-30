#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 22:10:30 2023

@author: orane
"""

import tgt
import glob
import csv
import os

def get_file_lst(path_folder):
    return glob.glob("../../" + path_folder + "*TextGrid" )

def read_files(file):
    path_textgrid =  file

    if os.path.isfile(path_textgrid):
        textgrid = tgt.io.read_textgrid(path_textgrid)
        return textgrid
    else :
        return False
   

def extract_interval_tier(textgrid):
    textgrid_mfa = textgrid.get_tier_by_name("phones")
    textgrid_annotator = textgrid.get_tier_by_name("correction")
    return textgrid_mfa,textgrid_annotator


def evaluate(tier_mfa, tier_annotator,tolerance_treshold=30):
    intervals_mfa = tier_mfa.intervals
    intervals_annotator = tier_annotator.intervals
    dico_accord = {"accord" : 0, "desaccord" : 0}
    #Si les TextGrids n'ont pas le même nombre d'intervalles, 
    #alors on ajoute la différence entre leur nombre d'intervalles au compte de désaccords
    #Ça ajoute des désaccords mais pas d'accords en plus alors que généralement quand il y a une 
    #Différence d'intervalles ce n'est qu'un problème local sur un mot et le reste de la transcription est bonne
    #ça pourrait peut-être expliquer le kappa plutôt bas ?
    if len(intervals_mfa) != len(intervals_annotator):
        #dico_accord["desaccord"] += abs(len(intervals_mfa) - len(intervals_annotator))
        pass
    else :

        for i in range(len(intervals_mfa)) :
            current_mfa_interval = intervals_mfa[i]
            current_annotator_interval = intervals_annotator[i]
            if (abs(current_mfa_interval.start_time - current_annotator_interval.start_time) <= tolerance_treshold / 1000 and
                abs(current_mfa_interval.end_time - current_annotator_interval.end_time) <= tolerance_treshold / 1000):
                dico_accord["accord"] += 1
            else : 
                dico_accord["desaccord"] += 1


    return dico_accord

def calculate_cohen_kappa(data):
    accord_count = data.get('accord', 0)
    desaccord_count = data.get('desaccord', 0)
    # Nombre total d'intervalles évalués 
    total = accord_count + desaccord_count
    # Proportion d'accords
    Po = accord_count / total
    # Calcul de l'accord dû au hasard, ici 50/50 car que deux catégories
    Pe = 0.5 * 0.5 + 0.5 * 0.5
    # Formule du Kappa de Cohen
    kappa = (Po - Pe) / (1 - Pe)

    return kappa        


    
def main():
    accord_total = {"accord" : 0, "desaccord" : 0}
    lst_folders = ["Corrections_mfa/ESLO2_ENT_1006/",
                   "Corrections_mfa/ESLO2_ENT_1037/",
                   "Corrections_mfa/ESLO2_ENT_1043/",
                   "Corrections_mfa/ESLO2_ENT_1071/",
                   "Corrections_mfa/ESLO2_ENT_1078/"]
    total_files = 0
    for folder in lst_folders :
        file_lst = get_file_lst(folder)
        total_files += len(file_lst)
        for file in file_lst :
            textgrid = read_files(file)
            tier_mfa,tier_annotator = extract_interval_tier(textgrid)
            accord_file = evaluate(tier_mfa, tier_annotator,tolerance_treshold=10)
            accord_total["accord"] += accord_file["accord"]
            accord_total["desaccord"] += accord_file["desaccord"]
    kappa = calculate_cohen_kappa(accord_total)
    
    print(f"Accords et désaccords sur l'ensemble des {total_files} TextGrids : ")
    print(accord_total)
    print(f"Kappa de Cohen : {kappa}")
        
            
            

if __name__ == "__main__" :
    main()