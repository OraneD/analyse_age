#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 14:59:43 2023

@author: orane
"""
import csv

with open("resultats_corpus_mfa.csv", "r") as csvfile :
    reader = csv.reader(csvfile)
    c = 0
    for row in reader :
        c += 1
    
with open("resultats_corpus_mfa_avec_md.csv", "r") as csvfile :
    reader = csv.reader(csvfile)
    c2 = 0
    for row in reader :
        c2 += 1
        
print(c)
print(c2)