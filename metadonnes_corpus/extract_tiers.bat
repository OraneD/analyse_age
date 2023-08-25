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
        
        IF !number! GEQ 1001 IF !number! LEQ 1017 (
        ) ELSE (
            "C:\Program Files\Praat.exe" "D:\\Memoire\\scripts\\tiers_without_overlaps.praat" "D:\\Memoire\\module_entretiens\\ESLO2_ENT_!number!\\" "%%b"
        )
    )
)

GOTO :EOF

