
@echo off

TITLE CAZADOR DE SUBTITULOS EN FILECATALYST


:start

echo.
echo *******************************
echo * CAZA SUBTITULOS DE CATALYST *
echo *******************************
echo.

:: ESTÁ EN EL GTW-3


L:

echo Cazando en \CATALYST
echo off
K:
for %%F in (*.stl) do (
echo %%F
move "K:\%%F" L:\
)


echo Esperando...

attrib -h "Z:\emision\*.*" /s /d

timeout 300

goto start

net use K: /delete
net use L: /delete