import tkinter as tk
from tkinter import filedialog
import os
import datetime

def seleccionar_directorio_salida():
    """
    Prompts the user to select a directory and stores the selected directory in the global variable 'directorio_salida'. 
    If a directory is selected, updates the text of the label 'etiqueta_directorio_salida' to display the selected directory.
    """
    global directorio_salida  # declare the global variable
    directorio_salida = filedialog.askdirectory()  # open a dialog box to select a directory
    if directorio_salida:  # check if a directory is selected
        etiqueta_directorio_salida.config(text="Directorio de salida seleccionado:\n" + directorio_salida)  # update the label text

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
#ventana.iconbitmap(r"programas\icono_datos.ico")
ventana.title("Seleccionar archivos y directorio de salida")

# Botón para seleccionar archivos
boton_seleccionar = tk.Button(ventana, text="Seleccionar archivos", command=seleccionar_archivos)
boton_seleccionar.pack(pady=10)

# Etiqueta para mostrar los archivos seleccionados
lista_archivos = []
etiqueta_archivos = tk.Label(ventana, text="Ningún archivo seleccionado")
etiqueta_archivos.pack()

# Botón para seleccionar directorio de salida
boton_seleccionar_directorio = tk.Button(ventana, text="Seleccionar directorio de salida", command=seleccionar_directorio_salida)
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
Archivo_log=open(directorio_salida + "\\" + "archivo_log" +".log","a",encoding="utf-8")
Archivo_log.write(fecha_actual.strftime("%d/%m/%Y%H:%M")+"\n")



# Recorre la lista de archivos seleccionados
for archivo in lista_archivos:
    # Abre cada archivo en modo lectura
    fichero = open(archivo, "r", encoding="utf-8")

    # Lee las primeras líneas que quieres omitir
    for _ in range(2):
        next(fichero)

    # Lee la siguiente línea que contiene información necesaria
    linea_circuito = fichero.readline()

    circuito = linea_circuito[10:13]

    linea_fecha = fichero.readline()

    year = linea_fecha[12:14]
    mes = linea_fecha[9:11]
    dia = linea_fecha[6:8]

    # Abre el archivo de salida en el directorio seleccionado
    # Se crea el fichero en modo escritura bajo el encode utf-8
    Archivo_salida=open(directorio_salida + "\\" + circuito+year+mes+dia+".rgt","w",encoding="utf-8")
    Archivo_salida.write(circuito+year+mes+dia+"\n")

    contador = 0

    # Otras operaciones para leer el archivo y escribir en el archivo de salida
    for _ in range(4):
        next(fichero)

    for linea in fichero:
        # Realiza operaciones en cada línea del archivo y escribe en el archivo de salida
        # Formato fichero

        print()

        TYPE = linea[1:6]
        START_TIME = linea[6:29]
        END_TIME = linea[29:52]
        MEDIA_ID = linea[52:85]
        EVENT = linea[85:106]
        TITLE = linea[106:139]
        SOM = linea[139:151]
        SEGMENT = linea[151:184]
        DURATION = linea[184:196]
        START_TYPE = linea[196:209]
        STRT_OFFSET = linea[209:221]
        END_TYPE = linea[221:234]
        END_OFFSET = linea[234:246]
        DEVICE_STREAM = linea[246:279]
        RECONCILE_KEY = linea[279:312]
        HOUSE_ID = linea[312:345]
        STATUS = linea[345:371]
        DEFAULT = "                                                                    "
        #TEST = "123456789012345678901234567890123456789012345678901234567890"

        # Comprobamos que sea media Event y el status no sea missed
        if EVENT == "Media Event          " and STATUS != "Missed                    ":
            # Iteramos sobre cada carácter en la cadena
            for caracter in RECONCILE_KEY:
                # Ignoramos los espacios en blanco
                if caracter == " ":
                    # Incrementamos el recuento para el carácter actual
                    RECONCILE_KEY = " " * 27
                    break

            A = START_TIME[11:22]
            B = MEDIA_ID[:18]
            C = DEFAULT[:2]
            D = TITLE[:32]
            E = DURATION[:11]
            F = RECONCILE_KEY[3:4]
            G = RECONCILE_KEY[1:2]
            if G == " " or G == "0":
                G = "2"
            H = RECONCILE_KEY[4:11]
            I = RECONCILE_KEY[11:14]
            J = DEFAULT[:5]
            K = RECONCILE_KEY[14:25]
            L = RECONCILE_KEY[25:27]
            M = DEFAULT[:14]
            N = DEFAULT[:2]
            O = DEFAULT[:2]
            P = RECONCILE_KEY[0:1]
            if P == " " or P == "0":
                P = "7"
            Q = DEFAULT[:1]
            R = RECONCILE_KEY[2:3]
            S = DEFAULT[:3]
            if S == "   ":
                S = "EST"
            T = DEFAULT[:1]
            U = DEFAULT[:4]
            V = DEFAULT[:1]
            W = DEFAULT[:1]
            ESPECIAL = DEFAULT[:2]
            X = RECONCILE_KEY[28:]
            # Iteramos sobre cada carácter en la cadena
            for caracter in X:
                # Ignoramos los espacios en blanco
                if caracter == " ":
                    break
                else:
                    X = X+":00"
                    break

            Y = DEFAULT[:1]

            # Escribimos en el archivo de salida la línea formateada correctamente.

            Archivo_salida.write(A +"  "+B +"  "+C+"  "+D+"  "+E+"  "+F+" "+G+H+"  "+I+"  "+J+"  "+K+"  "+L+"  "+M+"  "+N+" "+O+P+Q+R+S+T+U+V+W+ESPECIAL+" "+X+" "+Y+"\n")

            #print(A +"  "+B +"  "+C+"  "+D+"  "+E+"  "+F+" "+G+H+"  "+I+"  "+J+"  "+K+"  "+L+"  "+M+"  "+N+" "+O+P+Q+R+S+T+U+V+W+ESPECIAL+" "+X+" "+Y, end='')
        else:
            continue
    # Cerramos el archivo de entrada y el archivo de salida

    # Agregamos al fichero de log los ficheros que se ha procesado.

    nombre_archivo = os.path.basename(archivo)
    Archivo_log.write("     "+ nombre_archivo+"\n")

    fichero.close()




