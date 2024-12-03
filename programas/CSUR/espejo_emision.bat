@echo off

:: ESTÁ EN EL TC-1

setlocal enabledelayedexpansion
title ESPEJO EMISION
rem Cambia estas rutas según tus necesidades
set origen_emision=Z:\emision
set destino_emision=M:

:loop

set "file_list=Q:\MarinaList\MediaATV.txt"

FOR /F "skip=2 eol=(" %%A IN (Q:\MarinaList\MediaATV.txt) DO (

    :: Comprobar si el archivo ya existe en el destino
    IF NOT EXIST M:\%%A.mxf (

        :: Comprobar si el archivo existe en Z:\emision con extensión .mxf
        IF EXIST "Z:\emision\%%A.mxf" (
            xcopy /v Z:\emision\%%A.mxf M:\temp\

            :: Comprobar si xcopy tuvo éxito
            IF ERRORLEVEL 1 (
                echo         Error en la copia de %%A.mxf, eliminando archivo incompleto...
                del M:\temp\%%A.mxf
            ) ELSE (
                move M:\temp\%%A.mxf M:\
                echo         Archivo %%A.mxf copiado correctamente.
            )
        ) ELSE (
            :: Comprobar si existe el archivo sin extensión en Z:\emision
            IF EXIST "Z:\emision\%%A" (
                xcopy /v Z:\emision\%%A M:\temp\

                :: Comprobar si xcopy tuvo éxito
                IF ERRORLEVEL 1 (
                    echo         Error en la copia de %%A.mxf, eliminando archivo incompleto...
                    del M:\temp\%%A
                ) ELSE (
		    rename M:\temp\%%A %%A.mxf
                    move M:\temp\%%A.mxf M:\
                    echo         Archivo %%A.mxf copiado correctamente.
                )
            ) ELSE (
                echo         Archivo %%A.mxf no encontrado en Z:\emision.
            )
        )
    ) ELSE (
	 echo         Archivo %%A.mxf ya en M:\.
    )
)


echo.
echo El espejo de la carpeta emision se ha creado.
timeout /t 60
cls

goto loop
endlocal
