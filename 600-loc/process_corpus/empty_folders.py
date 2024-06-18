#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:56:29 2024

@author: odufour
"""
import glob
import os
print(os.getcwd())
folders = glob.glob("../Fabiole2_4Sec/*/*/*/")
print(folders)
nb = 0
with open("Fabiole2_empty.txt", "w") as file :
    for folder in folders :
            if os.listdir(folder) == [] :
                age = folder.split("/")[3]
                loc = folder.split("/")[4]
                sexe = folder.split("/")[2]
                print(f"Empty Folder : {loc}, {sexe}, {age}")
                file.write(f"Empty Folder : {loc}, {sexe}, {age}\n")
                nb += 1
            
           
    file.write(f"Total empty folder : {nb}")
