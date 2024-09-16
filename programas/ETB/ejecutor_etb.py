import configparser
import logging
import os
import tkinter as tk
from tkinter import filedialog
import datetime

def procesar_etb(lista_archivos: list):
    """
    Funcion donde vamos a procesar el fichero XML que viene desde Neptune para hacer el parseo a Automation.
    """

    # Obtener el directorio actual donde se ejecuta el script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(current_directory, 'registro.log')
    #print(f'El archivo de log se generará en: {log_file_path}')

    # Configurar el logger
    logging.basicConfig(
        level=logging.INFO,  # Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
        handlers=[
            logging.FileHandler(log_file_path),  # Archivo de log
            logging.StreamHandler()  # También imprimir en consola
        ]
    )

    configuracion = configparser.ConfigParser()

    # Leer el archivo de configuración
    try:
        if os.path.exists(r'D:\Traductor\Ejecutor\cf\config.conf'):
            configuracion.read(r'D:\Traductor\Ejecutor\cf\config.conf')
        elif os.path.exists(r'C:\Users\franciscojavier.mart\Documents\parseo\programas\ETB\cf\config.conf'):
            configuracion.read(r'C:\Users\franciscojavier.mart\Documents\parseo\programas\ETB\cf\config.conf')
        else:
            logging.error('Archivo de configuración no encontrado en ninguna de las rutas especificadas.')
            #raise FileNotFoundError('No se encontró el archivo de configuración.')
    except Exception as e:
        logging.exception('Error al leer el archivo de configuración: %s', e)

    # Cargamos los datos del archivo de configuración
    
    # Leemos el fichero que nos llega desde neptune



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

boton_salida = tk.Button(ventana, text="Ejecutar", command=procesar_etb(lista_archivos))
boton_salida.pack(pady=10)


# Ejecutar el bucle principal
ventana.mainloop()
    
