#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 23:26:20 2023

@author: orane
"""

import tgt
import glob
import csv
import os

def get_file_lst(path_folder):
    return glob.glob( path_folder + "*TextGrid" )

def read_files(file_mfa, file_1channel):
    path_mfa = file_mfa
    path_1channel = file_1channel

    if os.path.isfile(path_mfa) and os.path.isfile(path_1channel):
        textgrid_mfa = tgt.io.read_textgrid(path_mfa)
        textgrid_1channel = tgt.io.read_textgrid(path_1channel)
        return textgrid_mfa, textgrid_1channel
    else :
        return False
   

def extract_interval_tier(textgrid,textgrid_1channel):
    tier_mfa = textgrid.get_tier_by_name("phones")
    tier_1channel = textgrid_1channel.get_tier_by_name("phones")
    return tier_mfa, tier_1channel


def evaluate(tier_mfa, tier_1channel,tolerance_treshold=30):
    intervals_mfa = tier_mfa.intervals
    intervals_1channel = tier_1channel.intervals
    dico_accord = {"accord" : 0, "desaccord" : 0}
    #Si les TextGrids n'ont pas le même nombre d'intervalles, 
    #alors on ajoute la différence entre leur nombre d'intervalles au compte de désaccords
    #Ça ajoute des désaccords mais pas d'accords en plus alors que généralement quand il y a une 
    #Différence d'intervalles ce n'est qu'un problème local sur un mot et le reste de la transcription est bonne
    #ça pourrait peut-être expliquer le kappa plutôt bas ?
    if len(intervals_mfa) != len(intervals_1channel):
        dico_accord["desaccord"] += abs(len(intervals_mfa) - len(intervals_1channel))
        #pass
    else :

        for i in range(len(intervals_mfa)) :
            current_mfa_interval = intervals_mfa[i]
            current_1channel_interval = intervals_1channel[i]
            if (abs(current_mfa_interval.start_time - current_1channel_interval.start_time) <= tolerance_treshold / 1000 and
                abs(current_mfa_interval.end_time - current_1channel_interval.end_time) <= tolerance_treshold / 1000):
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
    lst_folders = ["ESLO2_DIA_1221",
                    "ESLO2_DIA_1222",
                    "ESLO2_DIA_1223",
                    "ESLO2_DIA_1224",
                    "ESLO2_DIA_1225",
                    "ESLO2_DIA_1226",
                    "ESLO2_DIA_1227",]
    total_files = 0
    
    for folder in lst_folders :
        accord_folder = {"accord" : 0, "desaccord" : 0}
        file_lst_mfa = sorted(get_file_lst(f"../../modules_ESLO/module_diachronie/diachronie_mfa/{folder}/{folder}_aligned/"))
        file_lst_1channel = sorted(get_file_lst(f"../../modules_ESLO/module_diachronie/diachronie_mfa_1channel/{folder}/{folder}_aligned/"))
        nb_files_folder = len(file_lst_1channel)
        total_files += nb_files_folder
        for i in range(len(file_lst_mfa)) :
            if file_lst_mfa[i].split("/")[-1] == file_lst_1channel[i].split("/")[-1]:
                textgrid_mfa, textgrid_1channel = read_files(file_lst_mfa[i], file_lst_1channel[i])
                #print(f"TextGrid MFA : {file_lst_mfa[i]}")
               # print(f"TextGrid 1channel : {file_lst_1channel[i]}")
    
                tier_mfa,tier_1channel = extract_interval_tier(textgrid_mfa, textgrid_1channel)
                accord_file = evaluate(tier_mfa, tier_1channel,tolerance_treshold=10)
                if accord_file["desaccord"] >= 5 :
                    print(file_lst_1channel)
                accord_folder["accord"] += accord_file["accord"]
                accord_folder["desaccord"] += accord_file["desaccord"]
                accord_total["accord"] += accord_file["accord"]
                accord_total["desaccord"] += accord_file["desaccord"]
        kappa_folder = calculate_cohen_kappa(accord_folder)
        print(f"Accord pour le dossier {folder} :")
        print(accord_folder)
        print(f"Kappa de Cohen pour le dossier : {kappa_folder}")
        print()
    kappa = calculate_cohen_kappa(accord_total)
    
    print(f"Accords et désaccords sur l'ensemble des {total_files} TextGrids : ")
    print(accord_total)
    print(f"Kappa de Cohen : {kappa}")
        
            
            

if __name__ == "__main__" :
    main()