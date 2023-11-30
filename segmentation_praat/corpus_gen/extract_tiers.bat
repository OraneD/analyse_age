@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

IF "%~1"=="" GOTO :EOF
SET "filename=%~1"
SET "linecount=0"

FOR /F "usebackq tokens=1,3 delims=," %%a IN ("%filename%") DO (
    SET /A "linecount+=1"
    
    IF !linecount!==1 (

    ) ELSE (
        FOR /F "tokens=3 delims=_ " %%i IN ("%%a") DO SET "number=%%i"
        REM Condition pour exclure certains dossiers
        IF !number! GEQ 1001 IF !number! LEQ 2000 (
        ) ELSE (
            "C:\Program Files\Praat.exe" "D:\\Memoire\\scripts\\tiers_without_overlaps.praat" "D:\\Memoire\\module_entretiens\\ESLO2_ENT_!number!\\" "%%b"
        )
    )
)

GOTO :EOF

REM Ce script prend en argument un fichier CSV avec les métadonnées du corpus
REM Il en extrait le nom du dossier du locuteur + l'identifiant de ce dernier (tier à récupérer dans les TextGrids)
REM Il lance ensuite le script praat qui extrait les tiers avec les deux arguments appropriés (nom du dossier + id du locuteur)