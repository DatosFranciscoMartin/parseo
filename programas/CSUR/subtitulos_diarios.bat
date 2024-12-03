
@echo off
setlocal EnableDelayedExpansion

:: ESTÁ EN EL POLISTREAM

TITLE MUEVE DE REPOSITORIO LOS DIARIOS

echo ***********************************
echo * PROGRAMA PARA COPIAR SUBTITULOS *
echo *          NECESARIOS             *
echo ***********************************
echo.


c:/PauseWithTimeout.exe 60

:rutina
cls

echo ***********************************
echo * PROGRAMA PARA COPIAR SUBTITULOS *
echo *          NECESARIOS             *
echo ***********************************
echo.

echo. >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
echo ******************************* >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
date/T >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
time/T >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
echo ******************************* >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
echo. >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
echo MOVER A LISTA >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"

FOR /F "skip=2" %%A IN (T:\SubsDiarios.txt) do (
	IF NOT EXIST C:\REPOSUBT\EMISION_ATV\%%A.stl (
		echo %%A >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
		copy C:\REPOSUBT\Backup_Subtitulos\%%A.stl C:\REPOSUBT\INCOMING >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"

	)
)
echo.
echo Esperando para mover a ATV...
c:/PauseWithTimeout.exe 300

cd C:\REPOSUBT\EMISION_CS1
del *.STL
del *.stl
del *.TIM
del *.tim
cd C:\REPOSUBT\EMISION_ATV
del *.CHK
del *.chk


echo MOVER A ATV >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"


for %%F in (*.stl) do (
	if not exist "S:\%%F" (
		echo %%F >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
		copy "C:\REPOSUBT\EMISION_ATV\%%F" S:\ >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"

	)
)

copy "C:\REPOSUBT\EMISION_ATV\" O:\ >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"

echo.
echo Esperando para recuperar lista de subtitulos...
c:/PauseWithTimeout.exe 300

echo.
echo Eliminando subtitulos no listados...
echo ELIMINAR NO LISTADOS >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"

REM Comparar archivos en EMISION_ATV con SubsDiarios.stl y eliminar los no listados
for %%F in (C:\REPOSUBT\EMISION_ATV\*.stl C:\REPOSUBT\EMISION_ATV\*.STL) do (
    set "found=0"
    set "filename=%%~nxF"
    set "filename=!filename:.STL=.stl!"

    for /F "skip=2" %%A in (T:\SubsDiarios.txt) do (
        set "listitem=%%A.stl"
        if /I "!filename!"=="!listitem!" set "found=1"
    )
    if "!found!"=="0" (
        echo Eliminando %%F >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
        del "%%F"
    )
)

for %%F in (S:\*.stl S:\*.STL) do (
    set "found=0"
    set "filename=%%~nxF"
    set "filename=!filename:.STL=.stl!"

    for /F "skip=2" %%A in (T:\SubsDiarios.txt) do (
        set "listitem=%%A.stl"
        if /I "!filename!"=="!listitem!" set "found=1"
    )
    if "!found!"=="0" (
        echo Eliminando %%F >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
        del "%%F"
    )
)

REM Comparar archivos en EMISION_CS1 con SubsDiarios.CHK y eliminar los no listados
for %%F in (C:\REPOSUBT\EMISION_CS1\*.chk C:\REPOSUBT\EMISION_CS1\*.CHK) do (
    set "found=0"
    set "filename=%%~nxF"
    set "filename=!filename:.CHK=.chk!"

    for /F "skip=2" %%A in (T:\SubsDiarios.txt) do (
        set "listitem=%%A.chk"
        if /I "!filename!"=="!listitem!" set "found=1"
    )
    if "!found!"=="0" (
        echo Eliminando %%F >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
        del "%%F"
    )
)

for %%F in (O:\*.stl O:\*.STL) do (
    set "found=0"
    set "filename=%%~nxF"
    set "filename=!filename:.STL=.stl!"

    for /F "skip=2" %%A in (T:\SubsDiarios.txt) do (
        set "listitem=%%A.stl"
        if /I "!filename!"=="!listitem!" set "found=1"
    )
    if "!found!"=="0" (
        echo Eliminando %%F >> "C:\REPOSUBT\FW\log_SUBSDIARIO.txt"
        del "%%F"
    )
)


cls
goto rutina