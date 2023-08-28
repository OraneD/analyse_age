@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

IF "%~1"=="" GOTO :EOF
SET "filename=%~1"
SET "linecount=0"

FOR /F "usebackq tokens=1,3 delims=," %%a IN ("%filename%") DO (
    SET /A "linecount+=1"
    
    IF !linecount!==1 (
        REM pour sauter le header
    ) ELSE (
        FOR /F "tokens=3 delims=_ " %%i IN ("%%a") DO SET "number=%%i"
        
        IF !number! GEQ 1000 IF !number! LEQ 1000 (
            REM exclusion de certains dossiers
        ) ELSE (
            "C:\Program Files\Praat.exe" "D:\\Memoire\\analyse_age\\scripts\\segmentation_praat\\segmentation_interval.praat" "D:\\Memoire\\corpus_1_tier\\ESLO2_ENTJEUN_!number!\\"
        )
    )
)

GOTO :EOF
REM ce script prend en argument le fichier csv avec les métadonnées du corpus
REM il en extrait les noms des dossiers à traiter pour les passer en arguments à un script praat
REM le script praat découpe les intervalles du fichier audio + TextGrid du locuteur et enregistre pour chaque intervalle le fichier audio + le TextGrid correspondant
REM il ignore les intervalles avec chevauchement
