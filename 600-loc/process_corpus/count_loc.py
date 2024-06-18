#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 12:10:39 2024

@author: odufour
"""

import glob
import os
from time import *

folders = glob.glob("../Fabiole2_4Sec/femme/young/*/")


nb_sec = 0
for folder in folders : 
    files = os.listdir(folder)
    if files != []:
        for file in files :
            nb_sec += 4
print(len(folders))            
print(strftime('%H %M %S', gmtime(nb_sec)))