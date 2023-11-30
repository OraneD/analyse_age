#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 21:04:11 2023

@author: orane
"""
import csv

def load_file(file):
    with open(file, "r") as csvfile :
        reader = csv.reader(csvfile, )
        times = [row[3] for row in reader]
        total_seconds = 0
        for time in times[1:]:
            minutes, seconds = map(int, time.split(":"))
            total_seconds += minutes * 60 + seconds
    hours = total_seconds // 3600
    minutes_left = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes_left:02d}:{seconds:02d}"


        

def main():
    print(load_file("../metadonnees_ESLO2_ENT_ENTJEUN.csv"))
    

    
if __name__ == "__main__":
    main()
    

        