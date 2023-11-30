#!/bin/bash
#Ce script va lancer l'alignement sur tous les corpus segmentés.
#le fichier "all_folders" contient tous les noms des dossiers à traiter
#pour chaque dossier, la corpus mfa est lancé et les TextGrids sont placées dans un dossier qui porte le nom du dossier traité + _aligned.

input_file="all_folders"

if [[ ! -f "$input_file" ]]; then
    echo "Le fichier 'all folder' n'existe pas."
    exit 1
fi

while IFS= read -r directory; do
    if [[ -d "$directory" ]]; then
        echo "Traitement du dossier : $directory"
        dir_name=$(basename "$directory")
        output_dir="${directory}/${dir_name}_aligned"
        mkdir -p "$output_dir"
        mfa align "$directory/" french_mfa french_mfa "$output_dir"
    else
        echo "Le répertoire '$directory' n'existe pas."
    fi
done < "$input_file"


