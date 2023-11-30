@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

IF "%~1"=="" GOTO :EOF
SET "filename=%~1"
SET "linecount=0"

FOR /F "usebackq tokens=1,2 delims=," %%a IN ("%filename%") DO (
    SET /A "linecount+=1"
    
    IF !linecount!==1 (
        REM pour sauter le header
        ECHO "ligne 1"
    ) ELSE (

        "C:\Program Files\Praat.exe" "D:\\Memoire\\modules_ESLO\\module_diachronie\\segmentation_interval.praat" "D:\\Memoire\\modules_ESLO\\module_diachronie\\diachronie_1_tier\\%%a\\"
    )
)

GOTO :EOF
REM ce script prend en argument le fichier csv avec les métadonnées du corpus
REM il en extrait les noms des dossiers à traiter pour les passer en arguments à un script praat
REM le script praat découpe les intervalles du fichier audio + TextGrid du locuteur et enregistre pour chaque intervalle le fichier audio + le TextGrid correspondant
REM il ignore les intervalles avec chevauchement
