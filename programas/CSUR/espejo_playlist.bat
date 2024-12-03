@echo off
setlocal enabledelayedexpansion
chcp 65001

:: ESTÁ EN EL TC-1

title ESPEJO PLAYLISTS
rem Cambia estas rutas según tus necesidades

set origen_trafico=Z:\TRAFICO\MarinaList
set destino_trafico=Q:\MarinaList

:loop

::robocopy "%origen_trafico%\CS1" "%destino_trafico%\CS1" /PURGE
::robocopy "%origen_trafico%\CS2" "%destino_trafico%\CS2" /PURGE
::robocopy "%origen_trafico%\CS3" "%destino_trafico%\CS3" /PURGE
robocopy "%origen_trafico%\ATV" "%destino_trafico%\ATV" /PURGE
::robocopy "%origen_trafico%\CS5" "%destino_trafico%\CS5" /PURGE
::robocopy "%origen_trafico%\CS1" "%destino_trafico%\CS1" /PURGE
::robocopy "%origen_trafico%\LISTA 7 WEB" "%destino_trafico%\LISTA 7 WEB" /PURGE
::robocopy "%origen_trafico%\Provinciales\ALMERÍA" "%destino_trafico%\Provinciales\ALMERÍA" /PURGE
::robocopy "%origen_trafico%\Provinciales\CÁDIZ" "%destino_trafico%\Provinciales\CÁDIZ" /PURGE
::robocopy "%origen_trafico%\Provinciales\CÓRDOBA" "%destino_trafico%\Provinciales\CÓRDOBA" /PURGE
::robocopy "%origen_trafico%\Provinciales\GRANADA" "%destino_trafico%\Provinciales\GRANADA" /PURGE
::robocopy "%origen_trafico%\Provinciales\HUELVA" "%destino_trafico%\Provinciales\HUELVA" /PURGE
::robocopy "%origen_trafico%\Provinciales\JAÉN" "%destino_trafico%\Provinciales\JAÉN" /PURGE
::robocopy "%origen_trafico%\Provinciales\MÁLAGA" "%destino_trafico%\Provinciales\MÁLAGA" /PURGE

echo.
echo El espejo de la carpeta trafico se ha creado.
timeout /t 1000
cls

goto loop

endlocal