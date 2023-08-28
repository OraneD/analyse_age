#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 00:18:54 2023

@author: orane
"""

import csv
import os 
from pathlib import Path
import mutagen
from mutagen.wave import WAVE
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime
from matplotlib.dates import DateFormatter
import time
from datetime import timedelta




print(os.getcwd())
#os.chdir("Memoire/analyse_age/metadonnes_corpus/")
print(os.getcwd())


########################
# conversion into time objects

def parse_ts(ts: str) -> timedelta:
     m, s = ts.split(':')
     return timedelta( minutes=int(m), seconds=float(s))
                  
def str_to_time(string) :
    return time.strptime(string, "%M:%S")

#########################


def csv_to_dico(file) :
    vingt_trentecinq = parse_ts("00:00")
    trentecinq_soixante = parse_ts("00:00")
    soixante_quatredix = parse_ts("00:00")


    with open(file, "r") as csvtime :
        reader = csv.reader(csvtime)
        next(reader)
        for row in reader :
            if 20 <= int(row[1]) < 35 :
                vingt_trentecinq += parse_ts(row[3])
            elif 35 <= int(row[1]) < 60 :
                trentecinq_soixante += parse_ts(row[3])
            elif 60 <= int(row[1]) < 90 :
                soixante_quatredix += parse_ts(row[3])
            else :
                print("locuteur non classé : " + row[0] + "âge : " + row[1])
        
                
        dico_tranche = {"20-35" : vingt_trentecinq,
                        "35-60" : trentecinq_soixante,
                        "60-90" : soixante_quatredix,

                        }
        return dico_tranche
                
dico = csv_to_dico("../metadonnes_corpus/age_time.csv")

def dico_to_graph(dico) :


    yvals = [k for k in dico.keys()]
    xvals = [v for v in dico.values()]
    zero = datetime.datetime(2018, 1, 1)
    time = [zero + t for t in xvals]
    zero = mdates.date2num(zero)
    time = [t - zero for t in mdates.date2num(time)]
    
    f = plt.figure()
    ax = f.add_subplot(1,1,1)
    
    ax.bar(yvals, time, bottom = zero)
    ax.yaxis_date()
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ylim = ax.get_ylim()
    ax.set_ylim(None, ylim[1]+0.1*np.diff(ylim))
    plt.title("Durées cumulées des échantillons par tranches d'âge du corpus")
    plt.ylabel("Durée (h, m, s)")
    plt.xlabel("Tranches d'âge")
    plt.show()

    
dico_to_graph(dico)
