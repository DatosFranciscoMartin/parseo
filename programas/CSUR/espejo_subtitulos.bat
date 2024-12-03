@echo off
setlocal enabledelayedexpansion
chcp 65001

Title ESPEJO_SUBTITULOS

:: ESTÁ EN EL TC-1


rem Cambia estas rutas según tus necesidades

set origen_subtitulos=Z:\DOLPHIN\subtitulos
set destino_subtitulos=S:

:loop

@echo off

robocopy "%origen_subtitulos%" "%destino_subtitulos%" *.stl /PURGE

echo.
echo El espejo de la carpeta subtitulos se ha creado.
timeout /t 300
cls

goto loop

endlocal

