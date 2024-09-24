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
    tipos_no_procesados = []
    
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
                            event1_2 = ET.SubElement(properties1, "event")
                            BlockName1 = ET.SubElement(properties1, "block")

                            title_element = event.find(f'ns:title', namespaces)
                            title = title_element.text if title_element is not None and title_element.text else ''

                            BlockName1.set("name", title)

                        else:

                            if event.get('type') == "LIVE":
                                # Se genera el evento Live

                                event1 = ET.SubElement(eventlist, "event")
                                event1.set("type", "Live")
                                properties1 = ET.SubElement(event1, "properties")
                                schedule1 = ET.SubElement(properties1, "schedule")

                                if event.find(f'ns:endtype', namespaces) is not None :
                                    if event.find(f'ns:endtype', namespaces).text == "NORM" :
                                        schedule1.set("endType", "Duration")
                                    elif event.find(f'ns:endtype', namespaces).text == "UNDEF":
                                        schedule1.set("endType", "Hold")

                                    duration_element = event.find(f'ns:duration', namespaces)
                                    duration = duration_element.text if duration_element is not None and duration_element.text else ''

                                    schedule1.set("endOffset", duration)

                                # Aqui ponemos el enrutado de los directos que tienen como fuente el mismo mediaid del evento
                                switch1 = ET.SubElement(properties1, "switch")

                                effect_element = event.find(f'ns:effect', namespaces)
                                effect = effect_element.text if effect_element is not None and effect_element.text else ''

                                rate_element = event.find(f'ns:rate', namespaces)
                                rate = rate_element.text if rate_element is not None and rate_element.text else ''
                                if rate == "Take":
                                    rate = "Cut"
                                elif rate == "TakeFade":
                                    rate = "Cut Fade"
                                elif rate =="FadeTake":
                                    rate = "Fade Cut"
                                elif rate == "TakeTake":
                                    rate = "V-Fade"

                                switch1.set("transition", effect)
                                switch1.set("rate", rate)
                                source1 = ET.SubElement(switch1, "source")
                                source1.set("type", "Logical")
                                logical1 = ET.SubElement(source1, "logical")

                                source_element = event.find(f'ns:source', namespaces)
                                source = source_element.text if source_element is not None and source_element.text else ''

                                logical1.set("name", source)
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

                                duration_element = event.find(f'ns:duration', namespaces)
                                duration = duration_element.text if duration_element is not None and duration_element.text else ''

                                schedule1.set("endOffset", duration)
                                media1 = ET.SubElement(properties1, "media")
                                media1.set("mediaType", "Video")

                                mediaid_element = event.find(f'ns:mediaid', namespaces)
                                mediaid = mediaid_element.text if mediaid_element is not None and mediaid_element.text else ''

                                media1.set("mediaName", mediaid)
                                mediaStream1 = ET.SubElement(properties1, "mediaStream")

                                som_element = event.find(f'ns:som', namespaces)
                                som = som_element.text if som_element is not None and som_element.text else ''

                                mediaStream1.set("som", som)
                                video1 = ET.SubElement(mediaStream1, "video")
                                video1.set("jobType", "Play")
                                segment1 = ET.SubElement(mediaStream1, "segment")
                                segment1.set("type", "User")
                                # Aqui ponemos el enrutado de las grabaciones que tienen como fuente el servidor por defecto
                                switch1 = ET.SubElement(properties1, "switch")

                                effect_element = event.find(f'ns:effect', namespaces)
                                effect = effect_element.text if effect_element is not None and effect_element.text else ''

                                rate_element = event.find(f'ns:rate', namespaces)
                                rate = rate_element.text if rate_element is not None and rate_element.text else ''
                                if rate == "Take":
                                    rate = "Cut"
                                elif rate == "TakeFade":
                                    rate = "Cut Fade"
                                elif rate =="FadeTake":
                                    rate = "Fade Cut"

                                switch1.set("transition", effect)
                                switch1.set("rate", rate)
                                source1 = ET.SubElement(switch1, "source")
                                source1.set("type", "Auto")
                                auto1 = ET.SubElement(source1, "auto")
                                auto1.set("type", "MediaStream")
                                # El destino lo estamos suponiendo como auto-PGM
                                destination1 = ET.SubElement(switch1, "destination")
                                destination1.set("type", "Auto")
                                auto1 = ET.SubElement(destination1, "auto")
                                auto1.set("type", "PGM")


                            # Se agrega etiquetas comunes de ambos casos
                            event1_2 = ET.SubElement(properties1, "event")

                            title_element = event.find(f'ns:title', namespaces)
                            title = title_element.text if title_element is not None and title_element.text else ''

                            houseid_element = event.find(f'ns:houseid', namespaces)
                            houseid = houseid_element.text if houseid_element is not None and houseid_element.text else ''

                            event1_2.set("title", title)
                            event1_2.set("houseId", houseid)
                            classifications1 = ET.SubElement(event1_2, "classifications")
                            classification1 = ET.SubElement(classifications1, "classification")
                            classification1.set("classification", "EventType")

                            category_element = event.find(f'ns:category', namespaces)
                            category = category_element.text if category_element is not None and category_element.text else ''

                            classification1.set("category", category)

                            if event.find(f'ns:starttype', namespaces).text == "SEQ":
                                schedule1.set("startType", "Sequential")
                            elif event.find(f'ns:starttype', namespaces).text == "FIX":
                                # Dividir onairdate y formatear al estilo YYYY-MM-DD
                                day, month, year = event.find(f'ns:onairdate', namespaces).text.split()
                                year = "20" + year  # Convertir el año '24' a '2024'

                                # Crear la fecha en formato ISO (YYYY-MM-DD)a
                                formatted_date = f"{year}-{month}-{day}"

                                # Combinar fecha y hora
                                start_offset = formatted_date+'T'+event.find(f'ns:onairtime', namespaces).text
                                schedule1.set("startType", "Fixed")
                                schedule1.set("startOffset", start_offset)
                            elif event.find(f'ns:starttype', namespaces).text == "MAN":
                                schedule1.set("startType", "Manual")

                            # Metemos el combinador de audio

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
                            customdata_node = event.find('.//ns:customdata', namespaces)

                            shmacro_element = event.find(f'ns:shmacro', namespaces)
                            shmacro = shmacro_element.text if shmacro_element is not None and shmacro_element.text else ''

                            shmacro_node = customdata_node.find(f'ns:shmacro', namespaces) if customdata_node is not None else None
                            trackpreset.set("name", shmacro_node.text if shmacro_node is not None else '')

                            # Generamos los eventos secundarios si existen

                            secondaryeventlistin = event.find('ns:secondaryeventlist', namespaces)
                            if secondaryeventlistin is not None:
                                #secondary_events = []
                                child_event = ET.SubElement(event1, "childEvents")
                                for secondary_event in secondaryeventlistin.findall('ns:secondaryevent', namespaces):

                                    type_element = secondary_event.get('type')
                                    type = type_element if type_element is not None else ''
                                    #if type != "ETB4 SUB" or not type.startswith("STR"):
                                    if ((type.startswith("ETB") or (type.startswith("STR"))) and (type.endswith("OFF") or type.endswith("ON"))) or type.startswith("I") and not type.endswith("9") and not type.endswith("SUB"):
                                        starttype = secondary_event.find('ns:starttype', namespaces).attrib if secondary_event.find('ns:starttype', namespaces) is not None else None
                                        endtype =secondary_event.find('ns:endtype', namespaces).attrib if secondary_event.find('ns:endtype', namespaces) is not None else None

                                        event_child_1 = ET.SubElement(child_event, "event")
                                        properties_child = ET.SubElement(event_child_1, "properties")
                                        schedule_child = ET.SubElement(properties_child, "schedule")
                                        switch_child = ET.SubElement(properties_child, "switch")

                                        if starttype is not None:
                                            if starttype.get('origin') == "+Start":
                                                schedule_child.set("startType", "+ParentStart")
                                            elif starttype.get('origin') == "-Start":
                                                schedule_child.set("startType", "-ParentStart")
                                            elif starttype.get('origin') == "+End":
                                                schedule_child.set("startType", "+ParentEnd")
                                            elif starttype.get('origin') == "-End":
                                                schedule_child.set("startType", "-ParentEnd")

                                            schedule_child.set("startOffset", starttype.get('offset', ''))


                                        if endtype is not None:
                                            if endtype.get('origin') == "+Start":
                                                schedule_child.set("endType", "+ParentStart")
                                            elif endtype.get('origin') == "-Start":
                                                schedule_child.set("endType", "-ParentStart")
                                            elif endtype.get('origin') == "+End":
                                                schedule_child.set("endType", "+ParentEnd")
                                            elif endtype.get('origin') == "-End":
                                                schedule_child.set("endType", "-ParentEnd")
                                            else:
                                                schedule_child.set("endType", "Duration")

                                            schedule_child.set("endOffset", endtype.get('offset', ''))

                                        if type.startswith("Intuition") or type == "Imagestore":

                                            # Si el evento secundario tiene 'customdata', extraer sus datos
                                            customdata_secondary = secondary_event.find('ns:customdata', namespaces)
                                            if customdata_secondary is not None:
                                                mediaStream_child = ET.SubElement(properties_child, "mediaStream")
                                                page = customdata_secondary.find('ns:page', namespaces).text if customdata_secondary.find(
                                                    'ns:page', namespaces) is not None else None
                                                layer = customdata_secondary.find('ns:lyr', namespaces).text if customdata_secondary.find(
                                                    'ns:lyr', namespaces) is not None else None
                                                template = customdata_secondary.find('ns:temp', namespaces).text if customdata_secondary.find(
                                                    'ns:temp', namespaces) is not None else None

                                            event_child_1.set("type", "VizRT")

                                            # Añadir el elemento 'media' dentro de 'properties'
                                            media_child = ET.SubElement(properties_child, "media")
                                            media_child.set("mediaType", "CG")

                                            if type == "Intuition":
                                                # Añadir los elementos 'cg' y 'allocation' dentro de 'mediaStream'
                                                cg = ET.SubElement(mediaStream_child, "cg")
                                                cg.set("layer", layer)
                                                cg.set("type", "Template")
                                                media_child.set("mediaName", template)
                                            else:
                                                cg = ET.SubElement(mediaStream_child, "cg")
                                                cg.set("layer", layer)
                                                cg.set("type", "Page")
                                                media_child.set("mediaName", page)


                                        elif type.startswith("ETB") or type.startswith("STR"):
                                        
                                            switch_child.set("transition", "Cut")
                                            switch_child.set("rate", "Fast")
                                            source1 = ET.SubElement(switch_child, "source")
                                            source1.set("type", "Fixed")
                                            fixed1 = ET.SubElement(source1, "fixed")
                                            destination1 = ET.SubElement(switch_child, "destination")
                                            destination1.set("type", "Fixed")
                                            fixed2 = ET.SubElement(destination1, "fixed")
                                            if "SUB" in type:
                                                #print(type)
                                                fixed2.set("port", "GPO-7")
                                                fixed1.set("device", "CIAB-4 GPO: Subtitle")
                                                if type.endswith("ON"):
                                                    event_child_1.set("type", "Subtitle GPI On")
                                                    fixed1.set("port", "On")
                                                elif type.endswith("OFF"):
                                                    event_child_1.set("type", "Subtitle GPI Off")
                                                    fixed1.set("port", "Off")
                                            else:
                                                fixed2.set("port", "GPO-10")
                                                fixed1.set("device", "CIAB-4 GPO: Logo")
                                                if type.endswith("ON"):
                                                    if type.startswith("ETB"):
                                                        event_child_1.set("type", "Logo GPI On")
                                                    else:
                                                        event_child_1.set("type", "Stream GPI On")
                                                    fixed1.set("port", "On")
                                                elif type.endswith("OFF"):
                                                    if type.startswith("ETB"):
                                                        event_child_1.set("type", "Logo GPI Off")
                                                    else:
                                                        event_child_1.set("type", "Stream GPI Off")
                                                    fixed1.set("port", "Off")
                                    else:
                                        tipos_no_procesados.append(type)
                    




                        comment = ET.SubElement(event1_2, "comment")
                        
                        eventnote_element = event.find(f'ns:eventnote', namespaces)
                        eventnote = eventnote_element.text if eventnote_element is not None and eventnote_element.text else ''

                        comment.text = eventnote

                       #################################################################################################3



#                       evento_data = {}
#
#                        # Extraer el tipo de evento
#                        evento_data['type'] = event.get('type')
#
#                        # Extraer los elementos hijos del evento
#                       for tag in ['starttype', 'onairtime', 'onairdate', 'mediaid', 'houseid', 'title', 'category',
#                                    'duration', 'som', 'effect', 'rate']:
#                            elemento = event.find(f'ns:{tag}', namespaces)
#                            evento_data[tag] = elemento.text if elemento is not None else None
#
#                        # Extraer los datos de 'customdata' si existen
#                        customdata = event.find('ns:customdata', namespaces)
#                        if customdata is not None:
#                            evento_data['customdata'] = {
#                                'shuffle': customdata.find('ns:shuffle', namespaces).text if customdata.find(
#                                    'ns:shuffle', namespaces) is not None else None,
#                                'shmacro': customdata.find('ns:shmacro', namespaces).text if customdata.find(
#                                    'ns:shmacro', namespaces) is not None else None,
#                            }
#
#                        # Extraer los eventos secundarios si existen
#                        secondaryeventlistin = event.find('ns:secondaryeventlist', namespaces)
#                        if secondaryeventlistin is not None:
#                            secondary_events = []
#                            for secondary_event in secondaryeventlistin.findall('ns:secondaryevent', namespaces):
#                                secondary_event_data = {
#                                    'type': secondary_event.get('type'),
#                                    'starttype': secondary_event.find('ns:starttype',
#                                                                      namespaces).attrib if secondary_event.find(
#                                        'ns:starttype', namespaces) is not None else None,
#                                    'endtype': secondary_event.find('ns:endtype',
#                                                                    namespaces).attrib if secondary_event.find(
#                                        'ns:endtype', namespaces) is not None else None,
#                                }
#
#                                # Si el evento secundario tiene 'customdata', extraer sus datos
#                                customdata_secondary = secondary_event.find('ns:customdata', namespaces)
#                                if customdata_secondary is not None:
#                                    secondary_event_data['customdata'] = {
#                                        'page': customdata_secondary.find('ns:page',
#                                                                          namespaces).text if customdata_secondary.find(
#                                            'ns:page', namespaces) is not None else None,
#                                        'lyr': customdata_secondary.find('ns:lyr',
#                                                                         namespaces).text if customdata_secondary.find(
#                                            'ns:lyr', namespaces) is not None else None,
#                                    }
#
#                                secondary_events.append(secondary_event_data)
#
#                            evento_data['secondary_events'] = secondary_events
#
#                        # Añadir el evento procesado a la lista de eventos
#                        eventos.append(evento_data)


                    # Mostrar la lista de eventos extraídos
                    #for i, evento in enumerate(eventos, start=1):
                    #    print(f"Evento {i}:")
                    #    for key, value in evento.items():
                    #        print(f"  {key}: {value}")


                    # Obtener una representación en cadena de texto del XML y formatear el XML
                    xml_str = ET.tostring(marinaPlaylist, encoding="iso-8859-1")
                    xml_formatted = xml.dom.minidom.parseString(xml_str).toprettyxml()
                    nombre_fichero = os.path.splitext(os.path.basename(archivo))[0]
                    #print(directorio_salida + "/" + nombre_fichero + "_formatted.xml")
                    with open(directorio_salida + "/" + nombre_fichero + "_formatted.mpl", "w", encoding="utf-8") as fichero_salida:
                        fichero_salida.write(xml_formatted)
                        

        except Exception as e:
            logging.exception('Error al leer el fichero: %s', archivo)
    datos_sin_repetidos = list(set(tipos_no_procesados))
    print(datos_sin_repetidos)
        



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
    
