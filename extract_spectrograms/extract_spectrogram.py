#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:54:34 2023

@author: orane
"""

import parselmouth
from parselmouth.praat import call
import tgt
import glob
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import random

def get_file_lst(path_folder):
    return glob.glob( path_folder)

def load_metadata(file):
    return [*csv.DictReader(open(file))]     

def extract_interval_tier(textgrid):
    return textgrid.get_tier_by_name("phones")


def process_files(sound,interval):
       label = interval.text
       if label == "s" :
           start_time = interval.start_time
           end_time = interval.end_time
           if abs(end_time - start_time) >= 0.12 :
               extract_s = sound.extract_part(from_time=start_time, to_time=end_time,preserve_times=False)
               # paramétrage pour les spectrogrammes calculés par Praat via les fonctions de Parselmouth
               max_frequency_spectrogram_Hz = 8000
               spectrogram = extract_s.to_spectrogram(maximum_frequency=max_frequency_spectrogram_Hz)
               return spectrogram,extract_s
           else :
               return False, False
       else :
           return False, False
       


def read_files(file):
    path_wav =  file
    path_textgrid = "../../corpus_mfa_1channel/"  + "".join(file.split("/")[3]) + "/" + "".join(file.split("/")[3]) + "_aligned/" + "".join(file.split("/")[4].replace(".wav", ".TextGrid"))
    if os.path.isfile(path_textgrid):
        sound = parselmouth.Sound(path_wav)
        textgrid = tgt.io.read_textgrid(path_textgrid)
        return sound, textgrid
    else :
        return False
    
def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)

    fig, ax = plt.subplots()
    cax = ax.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='gray_r')
    ax.set_xlim([X.min(), X.max()])
    ax.set_ylim([Y.min(), Y.max()])

    # Supprimer les axes et les étiquettes
    ax.axis('off')

    # Faire en sorte que le spectrogramme remplisse toute l'image
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Afficher l'image
    plt.show()
    
def export_smoothed_grayscale_spectrogram_with_zero_padding(spectrogram, image_width_inches, image_height_inches, resolution_dpi=None, dynamic_range=70, preemphasis_dB_by_octave=6, zero_padding_width_ratio=0, value_for_zero_padding=None):
  X, Y = spectrogram.x_grid(), spectrogram.y_grid()
  Xbins, Ybins = spectrogram.x_bins(), spectrogram.y_bins()
  Xmid = np.column_stack((Xbins[:,0],np.diff(Xbins,axis=1)/2)).sum(axis=1)
  Ymid = np.column_stack((Ybins[:,0],np.diff(Ybins,axis=1)/2)).sum(axis=1)
  # if requested, add pre-emphasis to boost higher frequency display (typical value for pre-emphasis = 6dB/octave)
  if(preemphasis_dB_by_octave>0):
    if(Ymid[0]<=0):
      logYmid = np.append(0,np.log2(Ymid[1::]))
    else:
      logYmid = np.log2(Ymid)
    intensityBoost_dB = (logYmid - min(logYmid))*preemphasis_dB_by_octave
    sg_db = (10 * np.log10(spectrogram.values))+intensityBoost_dB[:,np.newaxis]
  else:
    sg_db = 10 * np.log10(spectrogram.values)
  fig = plt.figure(frameon=False)
  fig.set_size_inches(image_width_inches,image_height_inches)
  ax = plt.Axes(fig, [0., 0., 1., 1.])
  ax.set_axis_off()
  fig.add_axes(ax)

  # interpolate values on both time and frequency dimensions using bivariate splines
  # (adapted from https://stackoverflow.com/a/32567022)
  f = interpolate.RectBivariateSpline(Xmid, Ymid, sg_db.T)
  Xnew = np.linspace(X[0], X[-1], 10*len(X))
  Ynew = np.linspace(Y[0], Y[-1], 10*len(Y))
  sg_bd_interp = f(Xnew, Ynew).T

  # add "zeros" (min value in image unless specified as argument value_for_zero_padding) on the right of the image if zero_padding_width_ratio is over 0 and below 1
  if(zero_padding_width_ratio>0 and zero_padding_width_ratio<1):
    if(value_for_zero_padding==None):
      value_for_zero_padding=np.min(sg_bd_interp)
    n_rows = sg_bd_interp.shape[0]
    n_cols = sg_bd_interp.shape[1]
    n_added_cols = int(np.round(n_cols * zero_padding_width_ratio / (1 - zero_padding_width_ratio)))
    added_zeros = np.ones((n_rows, n_added_cols))*value_for_zero_padding
    zero_padded_sg_bd_interp = np.flipud(np.concatenate((sg_bd_interp,added_zeros), axis = 1))
  else:
    zero_padded_sg_bd_interp = np.flipud(sg_bd_interp)

  ax.imshow(zero_padded_sg_bd_interp, aspect="auto", cmap="gray_r", vmin=sg_db.max() - dynamic_range, vmax=None)
  plt.show()
  
def export_grayscale_spectrogram_with_zero_padding(spectrogram,filename, image_width_inches, image_height_inches, resolution_dpi=None, dynamic_range=70, zero_padding_width_ratio=0, value_for_zero_padding=None):
  X, Y = spectrogram.x_grid(), spectrogram.y_grid()
  sg_db = 10 * np.log10(spectrogram.values)

  # add "zeros" (min value in image unless specified as argument value_for_zero_padding) on the right of the image if zero_padding_width_ratio is over 0 and below 1
  if(zero_padding_width_ratio>0 and zero_padding_width_ratio<1):
    if(value_for_zero_padding==None):
      value_for_zero_padding=np.min(sg_db)
    n_rows = sg_db.shape[0]
    n_cols = sg_db.shape[1]
    n_added_cols = int(np.round(n_cols * zero_padding_width_ratio / (1 - zero_padding_width_ratio)))
    added_zeros = np.ones((n_rows, n_added_cols))*value_for_zero_padding
    zero_padded_sg_db = np.flipud(np.concatenate((sg_db,added_zeros), axis = 1))
  else:
    zero_padded_sg_db = np.flipud(sg_db)

  fig = plt.figure(frameon=False)
  fig.set_size_inches(image_width_inches,image_height_inches)
  ax = plt.Axes(fig, [0., 0., 1., 1.])
  ax.set_axis_off()
  fig.add_axes(ax)
  ax.imshow(zero_padded_sg_db, aspect="auto", cmap="gray_r", vmin=sg_db.max() - dynamic_range, vmax=None)
  plt.savefig(filename, bbox_inches='tight', pad_inches=0, dpi = resolution_dpi)
  plt.close()


    

def main() : 
    
        largeur_images_pixels = 50
        hauteur_images_pixels = 50
        # conversion en pouces de la taille en pixels
        resolution_images_dpi = 100
        largeur_images_pouces = largeur_images_pixels/resolution_images_dpi
        hauteur_images_pouces = hauteur_images_pixels/resolution_images_dpi
        duree_max_signal_secondes = 0.12

        
        metadata = (load_metadata("../../metadonnees_ESLO2_ENT_ENTJEUN.csv"))
        len_folders = len(metadata)
        #Nombre de spectrogrammes à extraire désiré
        nb_spectrograms_extracted = 100
        
        for i, row in enumerate(metadata) :
            missing_file = 0
            folder = row["directory"]
            sexe = row["sexe"]
            age = row["age"]
            niveau_etude = row["niveau_etude"]
            categorie_professionnelle = row["categorie_professionnelle"]
            if int(age) < 30 :
                age_folder = "20-30"
            elif int(age) >= 30 and int(age) < 40 :
                age_folder = "30-40"
            elif int(age) >= 40 and int(age) < 50 :
                age_folder = "40-50"
            elif int(age) >= 50 and int(age) < 60 :
                age_folder = "50-60"
            elif int(age) >= 60 and int(age) < 70 :
                age_folder = "60-70"
            elif int(age) >= 70 and int(age) < 80 :
                age_folder = "70-80"
            elif int(age) >= 80 :
                age_folder = "80-90"
        
            print(f"Folder : {folder} ({i + 1}/{len_folders})")
            file_lst = get_file_lst(f"../../corpus_mfa_1channel/{folder}/*.wav")
            nb_files = len(file_lst)
            random.shuffle(file_lst)
            spectrograms_extracted = 0
            if spectrograms_extracted < nb_spectrograms_extracted :
                for file in file_lst:
                        if spectrograms_extracted < nb_spectrograms_extracted :
                            count_s = 0
                            if read_files(file) != False :
                                sound, textgrid = read_files(file)
                                tier = extract_interval_tier(textgrid)
                                for interval in tier.intervals :
                                    spectrogram,extract_s = process_files(sound,interval)
                                    if spectrogram != False :
                                        name_spectrogram = file.split("/")[-1].replace(".wav", f"_{count_s}.png")
                                        spectrogram_path = f"../Spectrograms/spectrograms_s_1channel/{age_folder}/{folder}/{name_spectrogram}"
                                       # print(spectrogram_path)
                                        #spectrogram_plot = draw_spectrogram(spectrogram)
                                        zeroPaddingWidthRatio = (duree_max_signal_secondes-extract_s.get_total_duration())/duree_max_signal_secondes
                                       # print(f"Total duration of /s/ : {extract_s.get_total_duration()} - Padding : {zeroPaddingWidthRatio}")
                                        #export_smoothed_grayscale_spectrogram_with_zero_padding(spectrogram, largeur_images_pouces, hauteur_images_pouces, resolution_images_dpi, preemphasis_dB_by_octave=6, zero_padding_width_ratio=zeroPaddingWidthRatio)
                                        export_grayscale_spectrogram_with_zero_padding(spectrogram,spectrogram_path, largeur_images_pouces, hauteur_images_pouces, resolution_images_dpi, zero_padding_width_ratio=zeroPaddingWidthRatio )
                                        count_s += 1
                                        spectrograms_extracted += 1
                            else :
                                missing_file += 1
                                continue
                        else :
                            break
            else :
                break

            nb_spectrograms = len(glob.glob(f"../Spectrograms/spectrograms_s_1channel/{age_folder}/{folder}/*.png"))
            print(f"Number of Spectrograms : {nb_spectrograms}")
            print(f"Completed - {missing_file}/{nb_files} missing TextGrid")
        


if __name__ == "__main__" :
    main()