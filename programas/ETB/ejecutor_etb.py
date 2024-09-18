import configparser
import logging
import os
import tkinter as tk
from tkinter import filedialog
import datetime
from datetime import timedelta, datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom

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

                    # Buscar el nodo 'list' y extraer el 'txdate'
                    txdate = root.find('.//{http://tempuri.org/playlist.xsd}txdate').text

                    # Transformamos la fecha de inicio a un objeto de tipo datetime
                    fecha_transformada = datetime.strptime(txdate, "%Y-%m-%d")

                    # Sumamos un dia a la fecha ya transformada
                    fecha_fin = fecha_transformada + timedelta(days=1)

                    # Transformamos la fecha de fin a una cadena de texto para usarla mas adelante
                    fecha_fin_transformada = fecha_fin.strftime("%Y-%m-%d")


                    # Crear el elemento raíz del XML, este debe de se de la siguiente forma, siempre va a ser asi:
                    marinaPlaylist = ET.Element("marinaPlaylist")
                    marinaPlaylist.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
                    marinaPlaylist.set("xsi:noNamespaceSchemaLocation", "./../../../playlist/playlist.xsd")
                    marinaPlaylist.set("version", "3.1")
                    marinaPlaylist.set("comment", "PebbleBeach Marina playlist generated by DatosMedia")
                    marinaPlaylist.set("StartTime", str(txdate) + "T01:00:00:00")
                    marinaPlaylist.set("EndTime", str(fecha_fin_transformada) + "T00:59:59:24")
                    properties = ET.SubElement(marinaPlaylist, "properties")
                    eventlist = ET.SubElement(marinaPlaylist, "eventList")

                    # Buscar el nodo 'eventlist' en el árbol XML
                    eventlistin = root.find('ns:eventlist', namespaces)

                    # Inicializar una lista para almacenar los eventos
                    eventos = []

                    # Recorrer todos los eventos dentro de 'eventlist'
                    for event in eventlistin.findall('ns:event', namespaces):

                        # Vamos creando el xml con los datos leidos en el evento iterado.
                        if event.get('type') == "MARKER":
                            if event.find(f'ns:category', namespaces).text == "BLOCKSTART":
                                event1 = ET.SubElement(eventlist, "event")
                                event1.set("type", "BlockStart")
                            elif event.find(f'ns:category', namespaces).text == "BLOCKEND":
                                event1 = ET.SubElement(eventlist, "event")
                                event1.set("type", "BlockEnd")

                            properties1 = ET.SubElement(event1, "properties")
                            BlockName1 = ET.SubElement(properties1, "block")
                            BlockName1.set("name", event.find(f'ns:title', namespaces).text)
                        else:
                            if event.get('type') == "LIVE":
                                # Se genera el evento Live
                                event1 = ET.SubElement(eventlist, "event")
                                event1.set("type", "Live")
                                properties1 = ET.SubElement(event1, "properties")
                                schedule1 = ET.SubElement(properties1, "schedule")
                                schedule1.set("endType", "Hold")
                                schedule1.set("endOffset", event.find(f'ns:duration', namespaces).text)
                                # Aqui ponemos el enrutado de los directos que tienen como fuente el mismo mediaid del evento
                                switch1 = ET.SubElement(properties1, "switch")
                                switch1.set("transition", event.find(f'ns:effect', namespaces).text)
                                switch1.set("rate", event.find(f'ns:rate', namespaces).text)
                                source1 = ET.SubElement(switch1, "source")
                                source1.set("type", "Logical")
                                logical1 = ET.SubElement(source1, "logical")
                                logical1.set("name", event.find(f'ns:source', namespaces).text)
                                # El destino lo estamos suponiendo como auto-PGM
                                destination1 = ET.SubElement(switch1, "destination")
                                destination1.set("type", "Auto")
                                auto1 = ET.SubElement(destination1, "auto")
                                auto1.set("type", "PGM")


                            elif event.get('type') == "MEDIA":
                                event1 = ET.SubElement(eventlist, "event")
                                event1.set("type", "PrimaryVideo")
                                properties1 = ET.SubElement(event1, "properties")
                                schedule1 = ET.SubElement(properties1, "schedule")
                                schedule1.set("endType", "Duration")
                                schedule1.set("endOffset", event.find(f'ns:duration', namespaces).text)
                                media1 = ET.SubElement(properties1, "media")
                                media1.set("mediaType", "Video")
                                media1.set("mediaName", event.find(f'ns:mediaid', namespaces).text)
                                mediaStream1 = ET.SubElement(properties1, "mediaStream")
                                mediaStream1.set("som", event.find(f'ns:som', namespaces).text)
                                video1 = ET.SubElement(mediaStream1, "video")
                                video1.set("jobType", "Play")
                                segment1 = ET.SubElement(mediaStream1, "segment")
                                segment1.set("type", "Media")
                                # Aqui ponemos el enrutado de las grabaciones que tienen como fuente el servidor por defecto
                                switch1 = ET.SubElement(properties1, "switch")
                                switch1.set("transition", event.find(f'ns:effect', namespaces).text)
                                switch1.set("rate", event.find(f'ns:rate', namespaces).text)
                                source1 = ET.SubElement(switch1, "source")
                                source1.set("type", "Auto")
                                auto1 = ET.SubElement(source1, "auto")
                                auto1.set("type", "MediaStream")
                                # El destino lo estamos suponiendo como auto-PGM
                                destination1 = ET.SubElement(switch1, "destination")
                                destination1.set("type", "Auto")
                                auto1 = ET.SubElement(destination1, "auto")
                                auto1.set("type", "PGM")
                                #if diccionario_interno['Tipo2']['NUMSEGMENTO'] != "0":
                                #    segment1.set("type", "Markup")
                                #    markup1 = ET.SubElement(segment1, "markup")
                                #    markup1.set("name", "TxSegments")
                                #    markup1.set("orderNo", diccionario_interno['Tipo2']['NUMSEGMENTO'])
                                #    mediaStream1.set("som", diccionario_interno['Tipo2']["HORINIEMI"].rstrip())
                                #    schedule1.set("endOffset", diccionario_interno['Tipo2']['HORFINEMI'].rstrip())

                            # Se agrega etiquetas comunes de ambos casos
                            event1_2 = ET.SubElement(properties1, "event")
                            event1_2.set("title", event.find(f'ns:title', namespaces).text)
                            classifications1 = ET.SubElement(event1_2, "classifications")
                            classification1 = ET.SubElement(classifications1, "classification")
                            classification1.set("classification", "EventType")
                            classification1.set("category", event.find(f'ns:category', namespaces).text)
                            schedule1.set("startType", "Sequential")
                            # Metemos el combinador de audio
                            customdata_node = event.find('.//ns:customdata', namespaces)
                            feature_1 = ET.SubElement(properties1, "features")
                            feature_audio1 = ET.SubElement(feature_1, "feature")
                            feature_audio1.set("type", "AudioShuffle")
                            properties_feature_audio = ET.SubElement(feature_audio1, "properties")
                            schedule_feature_audio = ET.SubElement(properties_feature_audio, "schedule")
                            schedule_feature_audio.set("startType", "+ParentStart")
                            schedule_feature_audio.set("startOffset", "00:00:00:00")
                            effect_feature_audio = ET.SubElement(properties_feature_audio, "effect")
                            effect_feature_audio.set("status", "On")
                            effect_feature_audio.set("type", "Audio Shuffle")
                            port_effect_feature_audio = ET.SubElement(effect_feature_audio, "port")
                            port_effect_feature_audio.set("type", "Auto")
                            auto_port_effect_feature_audio = ET.SubElement(port_effect_feature_audio, "auto")
                            auto_port_effect_feature_audio.set("type", "PGM")
                            audioshuffle = ET.SubElement(effect_feature_audio, "audioShuffle")
                            audioshuffle.set("type", "TrackPreset")
                            trackpreset = ET.SubElement(audioshuffle, "trackPreset")
                            trackpreset.set("name", customdata_node.find(f'ns:shmacro', namespaces).text)

                       #################################################################################################3



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
                        secondaryeventlistin = event.find('ns:secondaryeventlist', namespaces)
                        if secondaryeventlistin is not None:
                            secondary_events = []
                            for secondary_event in secondaryeventlistin.findall('ns:secondaryevent', namespaces):
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
                    #for i, evento in enumerate(eventos, start=1):
                    #    print(f"Evento {i}:")
                    #    for key, value in evento.items():
                    #        print(f"  {key}: {value}")


                    # Obtener una representación en cadena de texto del XML y formatear el XML
                    xml_str = ET.tostring(marinaPlaylist, encoding="iso-8859-1")
                    xml_formatted = xml.dom.minidom.parseString(xml_str).toprettyxml()
                    print(xml_formatted)

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
    
