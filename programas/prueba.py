import tkinter as tk
from tkinter import filedialog
import os
import datetime
import xml.etree.ElementTree as ET


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
    archivos = filedialog.askopenfilenames(filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))

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
ventana.geometry("600x400")
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
#                                       A partir de este punto se generan los archivos.                                        #
#                                                                                                                            #
#                                                                                                                            #
##############################################################################################################################


# Se genera el fichero de log

# se coge la fecha actual y se formatea para el nombre del archivo log en el directorio de salida seleccionado y se crea el archivo log
fecha_actual = datetime.date.today()
Archivo_log = open(directorio_salida + "\\" + "archivo_log" + ".log", "a", encoding="utf-8")
Archivo_log.write(fecha_actual.strftime("%d/%m/%Y-%H:%M") + "\n")

# Recorre la lista de archivos seleccionados
for archivo in lista_archivos:
    fichero = open(archivo, "r", encoding="utf-8")

    # Parsear el XML desde el archivo
    tree = ET.parse(fichero)
    root = tree.getroot()
    # Convertir el árbol XML a una cadena de texto
    #xml_str = ET.tostring(root, encoding='unicode', method='xml')

    DEFAULT = "*****************************************************"

    # Lee la siguiente línea que contiene información necesaria

    circuito = root.find('.//source').get('channelName')
    year = root.find('.//marinaAsRun').get('startTime')[2:4]
    mes = root.find('.//marinaAsRun').get('startTime')[5:7]
    dia = root.find('.//marinaAsRun').get('startTime')[8:10]

    # Abre el archivo de salida en el directorio seleccionado
    # Se crea el fichero en modo escritura bajo el encode utf-8
    Archivo_salida = open(directorio_salida + "\\" + circuito + year + mes + dia + ".rgt", "w", encoding="utf-8")
    Archivo_salida.write(circuito + year + mes + dia + "\n")

    contador = 0

        # Otras operaciones para leer el archivo y escribir en el archivo de salida
        for event in root.findall('.//eventList/event'):

            A = event.find('.//asRun').get('endTime').split('T')[1]
            B = event.find('.//properties/event').get('houseId')
            C = DEFAULT[:2]
            D = event.find('.//properties/event').get('title')
            E = event.find('.//asRun').get('duration')
            F = event.find('.//properties/event').get('reconcileKey')[3:4]
            G = event.find('.//properties/event').get('reconcileKey')[1:2]
            if G == " " or G == "0":
                G = "2"
            H = event.find('.//properties/event').get('reconcileKey')[4:11]
            I = event.find('.//properties/event').get('reconcileKey')[11:14]
            if event.find('.//properties/media').get('mediaName').startswith('B'):
                J = event.find('.//properties/media').get('mediaName')[1:6]
            else:
                J = DEFAULT[:5]
            K = event.find('.//properties/event').get('reconcileKey')[14:25]
            L = event.find('.//properties/event').get('reconcileKey')[25:27]
            if event.find('.//properties/event/comment') is not None:
                M = event.find('.//properties/event/comment').text[0:13]
            else:
                M = DEFAULT[:14]
            N = DEFAULT[:2]
            O = DEFAULT[:2]
            P = event.find('.//properties/event').get('reconcileKey')[0:1]
            if P == " " or P == "0":
                P = "7"
            Q = DEFAULT[:1]

            if event.find('.//properties/event').get('reconcileKey')[
               2:3] == "0":  # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                R = "0"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "1":  # SUBTITULADO == "S" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                R = "1"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "2":  # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                R = "2"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "3":  # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                R = "7"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "4":  # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                R = "3"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "5":  # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                R = "D"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "6":  # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                R = "B"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "7":  # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                R = "6"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "8":  # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                R = "9"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "9":  # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                R = "A"
            elif event.find('.//properties/event').get('reconcileKey')[
                 2:3] == "A":  # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                R = "C"

            "EST": "3-ST",
            "DST": "2-DL-ST",
            "MON": "1-MONO",
            "DUA": "2-DL-ST-DOLBY",
            "DP1": "7-DOLBY1",
            "DP2": "8-DOLBY2",
            "DP3": "Dolby PAR 3",
            "DG1": "5-DUAL5-6",
            "DG2": "6-DUAL3-4"

            S = DEFAULT[:3]
            #if S == "   ":
            #    S = "EST"
            T = DEFAULT[:1]
            U = DEFAULT[:4]
            V = DEFAULT[:1]
            W = DEFAULT[:1]
            ESPECIAL = DEFAULT[:2]
            X = event.find('.//properties/event').get('reconcileKey')[28:]
            Y = DEFAULT[:1]

            # Escribimos en el archivo de salida la línea formateada correctamente.

            Archivo_salida.write(
                A + "  " + B + "  " + C + "  " + D + "  " + E + "  " + F + " " + G + H + "  " + I + "  " + J + "  " + K + "  " + L + "  " + M + "  " + N + " " + O + P + Q + R + S + T + U + V + W + ESPECIAL + " " + X + " " + Y + "\n")

            # print(A +"  "+B +"  "+C+"  "+D+"  "+E+"  "+F+" "+G+H+"  "+I+"  "+J+"  "+K+"  "+L+"  "+M+"  "+N+" "+O+P+Q+R+S+T+U+V+W+ESPECIAL+" "+X+" "+Y, end='')
        else:
            continue
    # Cerramos el archivo de entrada y el archivo de salida

    # Agregamos al fichero de log los ficheros que se ha procesado.

    nombre_archivo = os.path.basename(archivo)
    Archivo_log.write("     " + nombre_archivo + "\n")

    fichero.close()
