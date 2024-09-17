import configparser
import logging
import os
import tkinter as tk
from tkinter import filedialog
import datetime
import xml.etree.ElementTree as ET

def procesar_etb(lista_archivos: list):
    """
    Funcion donde vamos a procesar el fichero XML que viene desde Neptune para hacer el parseo a Automation.
    """

    # Obtener el directorio actual donde se ejecuta el script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    #Generar el fichero de log en el directorio donde se ejecuta el script
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
        elif os.path.exists(r'C:\Scripts\ETB\cf'):
            configuracion.read(r'C:\Scripts\ETB\cf\config.conf')
        else:
            logging.error('Archivo de configuración no encontrado en ninguna de las rutas especificadas.')
            #raise FileNotFoundError('No se encontró el archivo de configuración.')
    except Exception as e:
        logging.exception('Error al leer el archivo de configuración: %s', e)

    extension_soportada = [".xml"]

    # Cargamos los datos del archivo de configuración
    
    # Leemos el fichero que nos llega desde neptune
    for archivo in lista_archivos:
        try:
            # Comprobar la extension del archivo
            extension = os.path.splitext(archivo)
            if extension[1] not in extension_soportada:
                logging.error("La extension del archivo no es soportada, se omite el archivo: %s", archivo)
            else:
                #print("Fichero con extension correcta")
                logging.info("Fichero con extension correcta, procesando...: %s", archivo)
                with open(archivo, "r", encoding="iso-8859-1"):
                    # Definir los namespaces utilizados en el XML
                    namespaces = {
                        'ns': 'http://tempuri.org/playlist.xsd'
                    }

                    tree = ET.parse(archivo)
                    root = tree.getroot()

                    # Buscar el nodo 'eventlist' en el árbol XML
                    eventlist = root.find('ns:eventlist', namespaces)

                    # Inicializar una lista para almacenar los eventos
                    eventos = []

                    # Recorrer todos los eventos dentro de 'eventlist'
                    for event in eventlist.findall('ns:event', namespaces):
                        evento_data = {}

                        # Extraer el tipo de evento
                        evento_data['type'] = event.get('type')

                        # Extraer los elementos hijos del evento
                        for tag in ['starttype', 'onairtime', 'onairdate', 'mediaid', 'houseid', 'title', 'category',
                                    'duration', 'som', 'effect', 'rate']:
                            elemento = event.find(f'ns:{tag}', namespaces)
                            evento_data[tag] = elemento.text if elemento is not None else None

                        # Extraer los datos de 'customdata' si existen
                        customdata = event.find('ns:customdata', namespaces)
                        if customdata is not None:
                            evento_data['customdata'] = {
                                'shuffle': customdata.find('ns:shuffle', namespaces).text if customdata.find(
                                    'ns:shuffle', namespaces) is not None else None,
                                'shmacro': customdata.find('ns:shmacro', namespaces).text if customdata.find(
                                    'ns:shmacro', namespaces) is not None else None,
                            }

                        # Extraer los eventos secundarios si existen
                        secondaryeventlist = event.find('ns:secondaryeventlist', namespaces)
                        if secondaryeventlist is not None:
                            secondary_events = []
                            for secondary_event in secondaryeventlist.findall('ns:secondaryevent', namespaces):
                                secondary_event_data = {
                                    'type': secondary_event.get('type'),
                                    'starttype': secondary_event.find('ns:starttype',
                                                                      namespaces).attrib if secondary_event.find(
                                        'ns:starttype', namespaces) is not None else None,
                                    'endtype': secondary_event.find('ns:endtype',
                                                                    namespaces).attrib if secondary_event.find(
                                        'ns:endtype', namespaces) is not None else None,
                                }

                                # Si el evento secundario tiene 'customdata', extraer sus datos
                                customdata_secondary = secondary_event.find('ns:customdata', namespaces)
                                if customdata_secondary is not None:
                                    secondary_event_data['customdata'] = {
                                        'page': customdata_secondary.find('ns:page',
                                                                          namespaces).text if customdata_secondary.find(
                                            'ns:page', namespaces) is not None else None,
                                        'lyr': customdata_secondary.find('ns:lyr',
                                                                         namespaces).text if customdata_secondary.find(
                                            'ns:lyr', namespaces) is not None else None,
                                    }

                                secondary_events.append(secondary_event_data)

                            evento_data['secondary_events'] = secondary_events

                        # Añadir el evento procesado a la lista de eventos
                        eventos.append(evento_data)

                    # Mostrar la lista de eventos extraídos
                    for i, evento in enumerate(eventos, start=1):
                        print(f"Evento {i}:")
                        for key, value in evento.items():
                            print(f"  {key}: {value}")
                    #Print de prueba
                    print(root.tag)
        except Exception as e:
            logging.exception('Error al leer el fichero: %s', archivo)
        



def seleccionar_directorio_salida():
    """
    Pide al usuario que seleccione un directorio y almacena el directorio seleccionado en la variable global 'directorio_salida'. 
    Si se selecciona un directorio, actualiza el texto de la etiqueta 'etiqueta_directorio_salida' para mostrar el directorio seleccionado. 
    """
    global directorio_salida  # declare the global variable
    directorio_salida = filedialog.askdirectory()  # open a dialog box to select a directory
    if directorio_salida:  # check if a directory is selected
        etiqueta_directorio_salida.config(text="Directorio de salida seleccionado:\n" + directorio_salida)  # update the label text

def seleccionar_archivos():
    """
    Pide al usuario que seleccione varios archivos y amplía la lista de archivos con los seleccionados.
    """
    # Prompt the user to select multiple files
    archivos = filedialog.askopenfilenames(filetypes=(("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")))
    
    # If files were selected, extend the list of files with the selected ones
    if archivos:
        lista_archivos.extend(archivos)
        actualizar_etiqueta_archivos()

def actualizar_etiqueta_archivos():
    """
    Actualiza la etiqueta 'etiqueta_archivos' con el texto "Archivos seleccionados:" seguido de los elementos de 'lista_archivos' unidos por nuevas líneas.
    
    Args:
        None
    
    Returns:
        None
    """
    # Update the text of etiqueta_archivos
    etiqueta_archivos.config(text="Archivos seleccionados:\n" + "\n".join(lista_archivos))

def salir():
    """
    Esta función cierra la ventana.
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
ventana.geometry("800x500")
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

# Boton para borrar la seleccion de archivos
boton_borrar = tk.Button(ventana, text="Borrar selección", command=lambda: (etiqueta_archivos.config(text="Ningún archivo seleccionado"), lista_archivos.clear()))
boton_borrar.pack(pady=10)

# Botón para ejecutar la funcion
Boton_ejecutar = tk.Button(ventana, text="Ejecutar", command=lambda: procesar_etb(lista_archivos))
Boton_ejecutar.pack(pady=10)

# Botón para cerrar la ventana
Boton_cerrar = tk.Button(ventana, text="Cerrar", command=salir)
Boton_cerrar.pack(pady=10)

# Ejecutar el bucle principal
ventana.mainloop()
    
