#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 17:54:22 2023

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
os.chdir("../")

print(os.getcwd())
corpus = Path("module_entretiens/")


def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
  
    return hours, mins, seconds  # returns the duration
  

def files_time() :
#csvfile id-locuteur, age, time
    
    with open("module_entretiens/metadonnees/age_time.csv", "w") as csvtime :
        writer = csv.writer(csvtime)
        for dossier in corpus.iterdir() :
            for file in dossier.iterdir() :
                if str(file).endswith(".wav") :
                    audio = WAVE(file)
                    audio_info = audio.info
                    length = int(audio_info.length)
                    hours, mins, seconds = audio_duration(length)
                    
                    with open('module_entretiens/metadonnees/module_entretiens.csv') as csvfile:
                        csvreader = csv.reader(csvfile)
                        for row in csvreader :
                            if row[0] == str(file).split("/")[1] :
                                time = datetime.time(hours,mins, seconds)
                                print(row[3], str(file) + ' Total Duration: {}:{}:{}'.format(hours, mins, seconds))
                                writer.writerow([row[0], row[3], time])
                          
#files_time()

########################
# conversion into time objects

def parse_ts(ts: str) -> timedelta:
     h, m, s = ts.split(':')
     return timedelta(hours=int(h), minutes=int(m), seconds=float(s))
                  
def str_to_time(string) :
    return time.strptime(string, "%H:%M:%S")

#########################


def csv_to_dico(file) :
    vingt_trente = parse_ts("00:00:00")
    trente_quarante = parse_ts("00:00:00")
    quarante_cinquante = parse_ts("00:00:00")
    cinquante_soixante = parse_ts("00:00:00")
    soixante_soixantedix = parse_ts("00:00:00")
    soixantedix_quatrevingt = parse_ts("00:00:00")
    quatrevingt_quatrevingtdix = parse_ts("00:00:00")
    quatrevingtdix_cent = parse_ts("00:00:00")

    with open(file, "r") as csvtime :
        reader = csv.reader(csvtime)
        for row in reader :
            if 20 <= int(row[1]) < 30 :
                vingt_trente += parse_ts(row[2])
            elif 30 <= int(row[1]) < 40 :
                trente_quarante += parse_ts(row[2])
            elif 40 <= int(row[1]) < 50 :
                quarante_cinquante += parse_ts(row[2])
            elif 50 <= int(row[1]) < 60 :
                cinquante_soixante += parse_ts(row[2])
            elif 60 <= int(row[1]) < 70 :
                soixante_soixantedix += parse_ts(row[2])
            elif 70 <= int(row[1]) < 80 :
                soixantedix_quatrevingt += parse_ts(row[2])
            elif 80 <= int(row[1]) < 90 :
                quatrevingt_quatrevingtdix += parse_ts(row[2])
            elif 90 <= int(row[1]) < 100 :
                quatrevingtdix_cent += parse_ts(row[2])
            else :
                print("locuteur non classé : " + row[0] + "âge : " + row[1])
        
                
        dico_tranche = {"20-30" : vingt_trente,
                        "30-40" : trente_quarante,
                        "40-50" : quarante_cinquante,
                        "50-60" : cinquante_soixante,
                        "60-70" : soixante_soixantedix,
                        "70-80" : soixantedix_quatrevingt,
                        "80-90" : quatrevingt_quatrevingtdix,
                        }
        return dico_tranche
                
dico = csv_to_dico("module_entretiens/metadonnees/age_time.csv")

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
    plt.title("Durées enregistrements par tranches d'âge Corpus ESLO2 - module entretiens")
    plt.ylabel("Durée")
    plt.xlabel("Tranches d'âge")
    plt.show()

    
dico_to_graph(dico)


