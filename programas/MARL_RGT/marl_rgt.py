import tkinter as tk
from tkinter import filedialog
import os
import datetime
import xml.etree.ElementTree as ET
import logging


def seleccionar_directorio_salida():
    """
    Prompts the user to select a directory and stores the selected directory in the global variable 'directorio_salida'.
    If a directory is selected, updates the text of the label 'etiqueta_directorio_salida' to display the selected directory.
    """
    global directorio_salida  # declare the global variable
    directorio_salida = filedialog.askdirectory()  # open a dialog box to select a directory
    if directorio_salida:  # check if a directory is selected
        etiqueta_directorio_salida.config(
            text="Directorio de salida seleccionado:\n" + directorio_salida)  # update the label text


def seleccionar_archivos():
    """
    Prompts the user to select multiple files and extends the list of files with the selected ones.
    """
    # Prompt the user to select multiple files
    archivos = filedialog.askopenfilenames(filetypes=(("Archivos de AsRun_xml", "*.marl"), ("Todos los archivos", "*.*")))

    # If files were selected, extend the list of files with the selected ones
    if archivos:
        lista_archivos.extend(archivos)
        actualizar_etiqueta_archivos()


def actualizar_etiqueta_archivos():
    """
    Updates the label 'etiqueta_archivos' with the text "Archivos seleccionados:"
    followed by the elements of 'lista_archivos' joined by newlines.

    Args:
        None

    Returns:
        None
    """
    # Update the text of etiqueta_archivos
    etiqueta_archivos.config(text="Archivos seleccionados:\n" + "\n".join(lista_archivos))


def salir():
    """
    This function closes the window.
    """
    ventana.destroy()


##############################################################################################################################
#                                                                                                                            #
#                                                                                                                            #
#                                       A partir de este punto se genera la interfaz.                                        #
#                                                                                                                            #
#                                                                                                                            #
##############################################################################################################################


# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1000x700")
# ventana.iconbitmap(r"programas\icono_datos.ico")
ventana.title("Seleccionar archivos y directorio de salida")

# Botón para seleccionar archivos
boton_seleccionar = tk.Button(ventana, text="Seleccionar archivos", command=seleccionar_archivos)
boton_seleccionar.pack(pady=10)

# Etiqueta para mostrar los archivos seleccionados
lista_archivos = []
etiqueta_archivos = tk.Label(ventana, text="Ningún archivo seleccionado")
etiqueta_archivos.pack()

# Botón para seleccionar directorio de salida
boton_seleccionar_directorio = tk.Button(ventana, text="Seleccionar directorio de salida",
                                         command=seleccionar_directorio_salida)
boton_seleccionar_directorio.pack(pady=10)

# Etiqueta para mostrar el directorio de salida seleccionado
etiqueta_directorio_salida = tk.Label(ventana, text="Ningún directorio de salida seleccionado")
etiqueta_directorio_salida.pack()

# Botón para salir

boton_salida = tk.Button(ventana, text="Ejecutar", command=salir)
boton_salida.pack(pady=10)

# Ejecutar el bucle principal
ventana.mainloop()

##############################################################################################################################
#                                                                                                                            #
#                                                                                                                            #
#                                       A partir de este punto se generan los archivos.                                      #
#                                                                                                                            #
#                                                                                                                            #
##############################################################################################################################


# Se genera el fichero de log

# se coge la fecha actual y se formatea para el nombre del archivo log en el directorio de salida seleccionado y se crea el archivo log
fecha_actual = datetime.date.today()
logging.basicConfig(filename=directorio_salida +'\\'+'registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Recorre la lista de archivos seleccionados
for archivo in lista_archivos:
    fichero = open(archivo, "r", encoding="utf-8")

    # Parsear el XML desde el archivo
    tree = ET.parse(fichero)
    root = tree.getroot()

    DEFAULT = "                                                                    "

    # Lee la siguiente línea que contiene información necesaria

    circuito = root.find('.//source').get('channelName')
    year = root.get('startTime')[2:4]
    mes = root.get('startTime')[5:7]
    dia = root.get('startTime')[8:10]
    nombre_fichero = circuito + year + mes + dia + ".rgt"

    # Abre el archivo de salida en el directorio seleccionado
    # Se crea el fichero en modo escritura bajo el encode utf-8
    Archivo_salida = open(directorio_salida + "\\" + nombre_fichero, "w", encoding="utf-8")
    Archivo_salida.write(circuito + year + mes + dia + "\n")

    logging.info(f"Archivo procesado: {archivo} --> Destino del fichero: {directorio_salida}\{nombre_fichero}")

    contador = 0

    # Otras operaciones para leer el archivo y escribir en el archivo de salida
    for event in root.findall('.//eventList/event'):
        if event.get('type') != "Comment":
            
            try:
                if event.get('enabled') == 'false' or event.find('.//asRun').get('result') in ["Descheduled", "Missed", "User Abort", "List Abort", "List Preempt"]:
                    Q = "6"
                elif event.find('.//properties/event').get('reconcileKey') is not None and not (len(event.find('.//properties/event').get('reconcileKey')) == 46 or len(event.find('.//properties/event').get('reconcileKey')) == 55):
                    Q = "5"
                else:
                    Q = " "
            except AttributeError:
                Q = " "

            try:
                A = event.find('.//asRun').get('startTime').split('T')[1]
            
            except AttributeError:
                A = DEFAULT[:11]

            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5":

                    if  event.get('type') == "Live" and Q == " ":
                        B = event.find('.//properties/event').get('reconcileKey')[18:36].replace("*", " ")
                    else:
                        B = event.find('.//properties/media').get('mediaName')
                        #B = event.find('.//properties/event').get('reconcileKey')[14:22]
                else:
                    B = DEFAULT[:18]
            except AttributeError:
                B = DEFAULT[:18]

            if event.find('.//properties/mediaStream/segment/markup') is not None:
                C = event.find('.//properties/mediaStream/segment/markup').get('orderNo')
            else:
                C = DEFAULT[:2]

            try:
                if event.find('.//properties/event').get('title') is not None:

                    D = event.find('.//properties/event').get('title')[:32]
                else:
                    D = DEFAULT[:32]
            except AttributeError:
                D = DEFAULT[:32]
            
            if event.find('.//asRun').get('duration') is not None and len(event.find('.//asRun').get('duration')) == 11:
                E = event.find('.//asRun').get('duration')
            else:
                E = DEFAULT[:11]

            tipos_de_eventos = {"Ajustes": "A", "Publicidad": "B", "Complementos": "C", "Desconexiones": "D", "Episodios": "E", "Programa": "P"}

            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5":

                    F = event.find('.//properties/event').get('reconcileKey')[0:1].replace("*", " ")
                    if F == "*":
                        F == " "
                else:
                    # Agregar diccionario con category
                    tipo_categoria = event.find('.//properties/event/classifications/classification').get('category')
                    F = tipos_de_eventos[tipo_categoria]
            except AttributeError:
                F = DEFAULT[:1]
            # En caso de no tenerlo en el reconcileKey, tenemos que preguntar por el diccionario de categorías para mapearlo.

            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 46:
                    G = event.find('.//properties/event').get('reconcileKey')[2:3].replace("*", " ")
                    if G == "*" or G == "0":
                        G = "2"
                else:
                    G = DEFAULT[:1]
            except AttributeError:
                G = DEFAULT[:1]
            
            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and len(event.find('.//properties/event').get('reconcileKey')) == 55:
                    H = event.find('.//properties/event').get('reconcileKey')[3:10].replace("*", " ")
                else:
                    H = DEFAULT[:7]
            except AttributeError:
                H = DEFAULT[:7]
            
            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 55:
                    I = event.find('.//properties/event').get('reconcileKey')[12:15].replace("*", " ")
                    if I == "    ":
                        I = DEFAULT[:3]                  
                else:
                    I = DEFAULT[:3]
            except AttributeError:
                I = DEFAULT[:3]

            #print(event.find('.//properties/media').get('mediaName'))
            try:
                if event.find('.//properties/media').get('mediaName') is not None and event.find('.//properties/media').get('mediaName').startswith("B"):
                    J = event.find('.//properties/media').get('mediaName')[1:6]
                else:
                    J = DEFAULT[:5]
            except AttributeError:
                J = DEFAULT[:5]
            
            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 55:
                    K = event.find('.//properties/event').get('reconcileKey')[24:35].replace("*", " ")
                else:
                    K = DEFAULT[:11]
            except AttributeError:
                K = DEFAULT[:11]
            
            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 55:
                    L = event.find('.//properties/event').get('reconcileKey')[37:39].replace("*", " ")
                else:
                    L = DEFAULT[:2]
            except AttributeError:
                L = DEFAULT[:2]

            if event.find('.//properties/event/comment') is not None:
                M = event.find('.//properties/event/comment').text[0:14]
            else:
                M = DEFAULT[:14]


            graficos_xml = event.findall('.//childEvents/event/properties/media')[:2]

            N = DEFAULT[:2]
            O = DEFAULT[:2]

            for index, grafico_xml in enumerate(graficos_xml):
                if index == 0:
                    if grafico_xml.get('mediaName')[-2:]:
                        N = grafico_xml.get('mediaName')[-2:]
                if index == 1:
                    if grafico_xml.get('mediaName')[-2:]:
                        O = grafico_xml.get('mediaName')[-2:]

            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 46:
                    P = event.find('.//properties/event').get('reconcileKey')[1:2].replace("*", " ")
                    if P == " " or P == "0":
                        P = "7"
                else:
                    P = DEFAULT[:1]
            except AttributeError:
                P = DEFAULT[:1]
            
            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 46:

                    #if event.find('.//properties/event').get('reconcileKey')[
                    #   2:3] == "0":  # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    #    R = "0"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "1":  # SUBTITULADO == "S" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    #    R = "1"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "2":  # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    #    R = "2"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "3":  # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    #    R = "7"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "4":  # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    #    R = "3"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "5":  # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    #    R = "D"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "6":  # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    #    R = "B"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "7":  # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    #    R = "6"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "8":  # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    #    R = "9"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "9":  # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    #    R = "A"
                    #elif event.find('.//properties/event').get('reconcileKey')[
                    #     2:3] == "A":  # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    #    R = "C"

                    # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " "
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "*" and event.find('.//properties/event').get('reconcileKey')[6:7] == "*" and event.find('.//properties/event').get('reconcileKey')[7:8] == "*":
                        R = "0"

                    # SUBTITULADO == "S" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "S" and event.find('.//properties/event').get('reconcileKey')[6:7] == "*" and event.find('.//properties/event').get('reconcileKey')[7:8] == "*":
                        R = "1"

                    # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "*" and event.find('.//properties/event').get('reconcileKey')[6:7] != "*" and event.find('.//properties/event').get('reconcileKey')[7:8] == "*":
                        R = "2"

                    # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "*" and event.find('.//properties/event').get('reconcileKey')[6:7] == "*" and event.find('.//properties/event').get('reconcileKey')[7:8] != "*":
                        R = "7"

                    # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "S" and event.find('.//properties/event').get('reconcileKey')[6:7] != "*" and event.find('.//properties/event').get('reconcileKey')[7:8] == "*":
                        R = "3"

                    # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS !=
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "*" and event.find('.//properties/event').get('reconcileKey')[6:7] != "*" and event.find('.//properties/event').get('reconcileKey')[7:8] != "*":
                        R = "D"

                    # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "S" and event.find('.//properties/event').get('reconcileKey')[6:7] != "*" and event.find('.//properties/event').get('reconcileKey')[7:8] != "*":
                       R = "B"

                    # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "I" and event.find('.//properties/event').get('reconcileKey')[6:7] == "*" and event.find('.//properties/event').get('reconcileKey')[7:8] == "*":
                        R = "6"

                    # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "I" and event.find('.//properties/event').get('reconcileKey')[6:7] != "*" and event.find('.//properties/event').get('reconcileKey')[7:8] == "*":
                        R = "9"

                    # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "I" and event.find('.//properties/event').get('reconcileKey')[6:7] == "*" and event.find('.//properties/event').get('reconcileKey')[7:8] != "*":
                        R = "A"

                    # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    if event.find('.//properties/event').get('reconcileKey')[5:6] == "I" and event.find('.//properties/event').get('reconcileKey')[6:7] != "*" and event.find('.//properties/event').get('reconcileKey')[7:8] != "*":
                        R = "C"

                else:
                    R = DEFAULT[:1]
            except AttributeError:
                R = DEFAULT[:1]

            mapeo_audio = {    
            "3-ST": "EST",
            "2-DL-ST": "DST",
            "1-MONO": "MON",
            "2-DL-ST-DOLBY": "DUA",
            "7-DOLBY1": "DP1",
            "8-DOLBY2": "DP2",
            "Dolby PAR 3": "DP3",
            "5-DUAL5-6": "DG1",
            "6-DUAL3-4": "DG2"
            }

            try:    
                if event.find('.//properties/features/feature/properties/effect/audioShuffle/trackPreset').get('name') is not None and event.find('.//properties/features/feature/properties/effect/audioShuffle/trackPreset').get('name') in ["3-ST", "2-DL-ST", "Dolby PAR 3", "6-DUAL3-4"]:
                    audio = event.find('.//properties/features/feature/properties/effect/audioShuffle/trackPreset').get('name')
                    S = mapeo_audio[audio]
                else:
                    S = DEFAULT[:3]
            except AttributeError:
                S = DEFAULT[:3]


            T = DEFAULT[:1]
            if event.find('.//childEvent/event/properties/event/comment') is not None and event.find('.//childEvent/event/properties/event/comment').text == "I":
                U = event.find('.//childEvent/event/properties/media').get('mediaName')
            else:
                U = DEFAULT[:4]

            V = DEFAULT[:1]

            if event.get('type') == "D":
                W = "D"
            else:
                W = DEFAULT[:1]
            ESPECIAL = DEFAULT[:2]

            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 46:
                    X = event.find('.//properties/event').get('reconcileKey')[38:].replace("*", " ")
                else:
                    X = DEFAULT[:8]
            except AttributeError:
                X = DEFAULT[:8]
            
            try:
                if event.find('.//properties/event').get('reconcileKey') is not None and Q != "5" and len(event.find('.//properties/event').get('reconcileKey')) == 46:
                    if event.find('.//properties/event').get('reconcileKey')[1:2] in ["1", "2"]:
                        Y = event.find('.//properties/event').get('reconcileKey')[1:2].replace("*", " ")
                    else:
                        Y = "0"
                else:
                    Y = "0"
            except AttributeError:
                Y = "0"

            # Escribimos en el archivo de salida la línea formateada correctamente.
            output_line = "{:<11}  {:<18}  {:<2}  {:<32}  {:<11}  {:<1} {:<1}{:<7}  {:<3}  {:<5}  {:<11}  {:<2}  {:<14}  {:<2} {:<2}{:<1}{:<1}{:<1}{:<3}{:<1}{:<4}{:<1}{:<1}{:<2}  {:<8}  {:<1}\n".format(
                str(A), str(B), str(C), str(D), str(E), str(F), str(G), str(H), str(I), str(J), str(K), str(L), str(M), str(N), str(O), str(P), str(Q), str(R), str(S), str(T), str(U), str(V), str(W), str(ESPECIAL), str(X), str(Y)
            )
            Archivo_salida.write(output_line)
    
    else:
        continue
