@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

IF "%~1"=="" GOTO :EOF
SET "filename=%~1"
SET "linecount=0"

FOR /F "usebackq tokens=1,2 delims=," %%a IN ("%filename%") DO (
    SET /A "linecount+=1"
    
    IF !linecount!==1 (
        REM première ligne, pas besoin
        ECHO "première ligne"    
    ) ELSE (
        "C:\Program Files\Praat.exe" "D:\\Memoire\\module_diachronie\\tiers_without_overlaps.praat" "D:\\Memoire\\module_diachronie\\%%a\\" "%%b"
    )
)

GOTO :EOF

REM Ce script prend en argument un fichier CSV avec les métadonnées du corpus
REM Il en extrait le nom du dossier du locuteur + l'identifiant de ce dernier (tier à récupérer dans les TextGrids)
REM Il lance ensuite le script praat qui extrait les tiers avec les deux arguments appropriés (nom du dossier + id du locateur)

