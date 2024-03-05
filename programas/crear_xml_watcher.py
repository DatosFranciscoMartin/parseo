import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
from datetime import timedelta, datetime
import time
import logging

# Se genera una lista de IDs especiales que se usara a la hora de procesar el logo branding
media_id_espciales = ["P0","P3","A5","P4","P5","P611PDS00049","P699EDS00006","P699EGS00121","P611PGS00595","P699PGS00568","P699PGS00872","P611PGS00547","P899PGS00064","P211PDS00033","P211PDS00034","P699PGS00961","P211PDS00036","P211EGS00006","P531PGS00057","P531PGS00056","P211EGS00007","P211PDS00037","P211EGS00008","P463PGS00057","P211EGS00009","P211PDS00038","P469PDS00102"]


# En esta parte del programa vamos a crear el watch folder para procesar los ficheros TRF

def seleccionar_directorio_a_monitorizar():
    """
    Esta función de Python pide al usuario que seleccione un directorio y almacena el directorio seleccionado en la variable global 'directorio_monitorizar'. 
    Si se selecciona un directorio, actualiza el texto de una etiqueta para mostrar el directorio seleccionado.
    """
    global directorio_monitorizar  
    directorio_monitorizar = filedialog.askdirectory()  
    if directorio_monitorizar:  
        etiqueta_directorio_monitorizar.config(text="Directorio a monitorizar seleccionado:\n" + directorio_monitorizar)

def seleccionar_directorio_salida():
    """
    seleccionar_directorio_salida que pide al usuario que seleccione un directorio y almacena el directorio seleccionado en la variable global directorio_salida. Si se selecciona un directorio, 
    actualiza el texto de la etiqueta directorio_salida para mostrar el directorio seleccionado.
    """
    global directorio_salida  
    directorio_salida = filedialog.askdirectory()  
    if directorio_salida:
        etiqueta_directorio_salida.config(text="Directorio de salida seleccionado:\n" + directorio_salida)  

def salir():
    """
    Esta funcion cierra la ventana.
    """
    ventana.destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("600x400")
#ventana.iconbitmap(r"programas\icono_datos.ico")
ventana.title("Seleccionar directorio a monitorizar y directorio de salida")

# Botón para seleccionar directorio a monitorizar
boton_seleccionar_directorio_a_monitorizar = tk.Button(ventana, text="Seleccionar directorio a monitorizar", command=seleccionar_directorio_a_monitorizar)
boton_seleccionar_directorio_a_monitorizar.pack(pady=10)

# Etiqueta para mostrar el directorio a monitorizar seleccionado
etiqueta_directorio_monitorizar = tk.Label(ventana, text="Ningún directorio de salida seleccionado")
etiqueta_directorio_monitorizar.pack()

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

# Directorio a monitorear
directorio_a_monitorear = directorio_monitorizar

# Agregado lineas de para generar un log en tiempo real
log_file = os.path.join(directorio_salida, "log.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M')


def procesar_archivo(archivo):
    """
    Este fragmento de código Python define una función procesar_archivo que procesa un archivo, en este caso seran ficheros .trf. Extrae información del archivo de entrada, manipula los datos y escribe la salida formateada en un nuevo archivo. 
    El código incluye operaciones como la lectura de líneas específicas, la extracción de subcadenas y la escritura de datos formateados en un archivo de salida. 
    También registra el nombre del fichero procesado e imprime un mensaje en la consola.
    """
    # Generamos el nombre del fichero para el log, eliminamos la ruta absoluta y nos quedamos solo con el nombre del fichero
    nombre_archivo = os.path.basename(archivo)
    logging.info(f"Archivo procesado: {nombre_archivo}")

    print("Procesando archivo:", archivo)

    with open(archivo, "r", encoding="utf-8") as fichero:

        # Nos saltamos la primera linea del fichero y sacamos sus datos.
        primera_linea = fichero.readline()
        
        # Generamos las variables de la primera linea del fichero
        LICOMINUTA = primera_linea[0:10]
        LICADENA = primera_linea[10:26].rstrip()
        LISEMANA = primera_linea[26:28]
        LIANIO = primera_linea[28:32]
        LIFECMINUT= primera_linea[32:40]

        # La fecha de inicio
        fecha_inicio = LIANIO + "-" + LIFECMINUT[3:5] + "-" + LIFECMINUT[:2]

        # Transformamos la fecha de inicio a un objeto de tipo datetime
        fecha_transformada = datetime.strptime(fecha_inicio, "%Y-%m-%d")

        # Sumamos un dia a la fecha ya transformada
        fecha_fin = fecha_transformada + timedelta(days=1)

        # Transformamos la fecha de fin a una cadena de texto para usarla mas adelante
        fecha_fin_transformada = fecha_fin.strftime("%Y-%m-%d")

        # Creamos un diccionario vacío en el que vamos a ir guardando diccionarios que van a corresponder a cada uno de los eventos que tenemos en los ficheros TRF, se guardarian solo los tiopos 1, 4 y 5 ya que los elementos
        # de tipo 2 y 3 siempre van dentro de los elementos de tipo 1
        eventos = {}

        # Generamos 3 contados que nos van a ayudar a generar el numero de eventos que vamos a tener, con los contadores de tipo nos ayuda a poder generar diccionarios dentro de los eventos de tipo 1
        contador = 0
        contador_tipo_3 = 0

        # Creamos la primera iteración sobre el fichero que hemos cargado anteriormente,
        for linea in fichero:

            # Primero comprobamos el tipo de evento que es mediante el primer caracter de la linea
            if linea[0:1] == '1':
                contador += 1

                # Aqui tenemos la logica que vamos a seguir con los eventos de tipo 1, en el que se puede ver como la siguiente informacion se extrae de la siguiente manera
                TIPOREG = linea[0:1]
                INDMULTI = linea[1:3]
                TICODELEMENMIN = linea[3:18]
                TITIPELEME = linea[18:19]
                TIHOINMIN = linea[19:30]  # HORA DE INICIO
                TIDUMINUT = linea[30:41]
                TITITELEME = linea[41:107]
                LENGUAJE_DE_SIGNOS = linea[107:108]
                AUDIODESCRIPCION = linea[108:109]
                RELACION_DE_ASPECTO = linea[110:111]
                TIPO_DE_AUDIO = linea[111:114]
                CALIFMORAL = linea[114:118]
                INDELEMFIJO = linea[118:119]

                if INDELEMFIJO == "F":
                    SCH_StartType = "Fixed"
                else:
                    SCH_StartType = "Sequential"

                CONTRATO = linea[119:126]
                PASE = linea[126:129]
                CODLOCALI = linea[129:132]
                NO_PA = linea[132:134]
                DIRGRAB = linea[134:135]
                SUBTITULADO = linea[135:136]
                INDLOGO = linea[136:137]
                NUMERO_DE_LOGO = linea[137:139]
                DISTINTIVO_DE_CALIFMORAL = linea[140:141]

                # Linea donde vamos a gener la reconcilekey

                if CALIFMORAL == "    ":
                    CLASIFICACION = "0"
                elif CALIFMORAL == "ERI ":
                    CLASIFICACION = "1"
                elif CALIFMORAL == "NR12":
                    CLASIFICACION = "2"
                elif CALIFMORAL == "NR13":
                    CLASIFICACION = "3"
                elif CALIFMORAL == "NR16":
                    CLASIFICACION = "4"
                elif CALIFMORAL == "NR18":
                    CLASIFICACION = "5"
                elif CALIFMORAL == "NR7 ":
                    CLASIFICACION = "6"
                elif CALIFMORAL == "PT  ":
                    CLASIFICACION = "7"
                elif CALIFMORAL == "SC  ":
                    CLASIFICACION = "8"
                elif CALIFMORAL == "X   ":
                    CLASIFICACION = "9"

                if SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    TXTAUD = "0"
                elif SUBTITULADO == "S" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    TXTAUD = "1"
                elif SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    TXTAUD = "2"
                elif SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    TXTAUD = "3"
                elif SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    TXTAUD = "4"
                elif SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    TXTAUD = "5"
                elif SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    TXTAUD = "6"
                elif SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    TXTAUD = "7"
                elif SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    TXTAUD = "8"
                elif SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    TXTAUD = "9"
                elif SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    TXTAUD = "A"

                # print(CLASIFICACION+RELACION_DE_ASPECTO+TXTAUD+TITIPELEME+CONTRATO+PASE+TICODELEMENMIN+TICODELEMENMIN[11:]+"_"+TIHOINMIN[:8])
                RECONCILEKEY = CLASIFICACION + RELACION_DE_ASPECTO + TXTAUD + TITIPELEME + CONTRATO + PASE + TICODELEMENMIN[:11] + TICODELEMENMIN[11:13] + "_" + TIHOINMIN[:8]
                # print(RECONCILEKEY.replace(" ", "*"))

                # Generamos el diccionario con la informacion que hemos extraid del fichero principal
                eventos[contador] = {
                    "TIPOREG": linea[0:1],
                    "INDMULTI": linea[1:3],
                    "TICODELEMENMIN": linea[3:18],
                    "TITIPELEME": linea[18:19],
                    "TIHOINMIN": linea[19:30],
                    "TIDUMINUT": linea[30:41],
                    "TITITELEME": linea[41:107],
                    "LENGUAJE_DE_SIGNOS": linea[107:108],
                    "AUDIODESCRIPCION": linea[108:109],
                    "RELACION_DE_ASPECTO": linea[110:111],
                    "TIPO_DE_AUDIO": linea[111:114],
                    "CALIFMORAL": linea[114:118],
                    "INDELEMFIJO": INDELEMFIJO,
                    "CONTRATO": linea[119:126],
                    "PASE": linea[126:129],
                    "CODLOCALI": linea[129:132],
                    "NO_PA": linea[132:134],
                    "DIRGRAB": linea[134:135],
                    "SUBTITULADO": linea[135:136],
                    "INDLOGO": linea[136:137],
                    "NUMERO_DE_LOGO": linea[137:139],
                    "DISTINTIVO_DE_CALIFMORAL": linea[140:141],
                    "SCH_StartType": SCH_StartType,
                    "RECONCILEKEY": RECONCILEKEY.replace(" ", "*")
                }

            # Aqui comprobamos si es de tipo 2, si es de tipo seguimos la siguiente logica para extraer la informacion.
            elif linea[0:1] == '2':

                # Inicializamos el contador de tipo 2 para ir contando los eventos de tipo 2

                # Aqui guardamos todos los campos que nos interesan dentro de un diccionario que vamos a guardar en el evento de tipo 1 con el numero de evento
                eventos[contador]["Tipo2"] = {
                    "TIPOREG": linea[0:1],
                    "TIPOCINTA": linea[1:2],
                    "CODCINTA": linea[2:12],
                    "HORINIEMI": linea[12:23],
                    "HORFINEMI": linea[23:34],
                    "NUMSEGMENTO": linea[34:35],
                    "ULTIMO": linea[35:36],
                    "Literal1": linea[37:39],
                    "HORA_ANUNCIADA": linea[40:48],
                    "Literal2": linea[50:52],
                    "NOCOMPUTA": linea[53:]
                }
            # Aqui comprobamos si es de tipo 3, si es de tipo seguimos la siguiente logica para extraer la informacion.
            elif linea[0:1] == '3':

                # Inicializamos el contador de tipo 3 para ir contando los eventos de tipo 3
                contador_tipo_3 += 1

                # Aqui guardamos todos los campos que nos interesan dentro de un diccionario que vamos a guardar en el evento de tipo 1 con el numero de evento
                eventos[contador]["Tipo3" + "_" + str(contador_tipo_3)] = {
                    "TIPOREG": linea[0:1],
                    "TIPO_DE_INSERCION": linea[1:2],
                    "NUMERO_DE_LA_INCRUSTACION": linea[3:7],
                    "HORA_DE_COMIENZO": linea[8:19].replace(".", ":"),
                    "DURACION": linea[20:31].replace(".", ":")
                }

            # Aqui comprobamos si es de tipo 4 o 5, si es de tipo 4 o 5 seguimos la siguiente logica para extraer la informacion.
            elif linea[0:1] in ['4', '5']:

                # En este caso, si usamos el contado de eventos para evitar que los tipo 4 y 5 esten en el mismo evento que los tipo 1
                contador += 1

                # Aqui guardamos todos los campos que nos interesan dentro de un diccionario que vamos a guardar en el evento de tipo 1 con el numero de evento
                eventos[contador] = {
                    "TIPOREG": linea[0:1],
                    "IDBLOQUE": linea[1:40] if linea[0:1] == '4' else None,
                    "ESPACIO": linea[1:2] if linea[0:1] == '5' else None,
                    "OBSERVACIONES": linea[2:34] if linea[0:1] == '5' else None
                }

        # Cerramos el fichero
        fichero.close()

        #for event, diccionario_interno in eventos.items():
        #    print(diccionario_interno)

        # Crear el elemento raíz del XML, este debe de se de la siguiente forma, siempre va a ser asi:
        marinaPlaylist = ET.Element("marinaPlaylist")
        marinaPlaylist.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        marinaPlaylist.set("xsi:noNamespaceSchemaLocation", "./../../../playlist/playlist.xsd")
        marinaPlaylist.set("version", "3.1")
        marinaPlaylist.set("comment", "PebbleBeach Marina playlist generated by DatosMedia")
        marinaPlaylist.set("StartTime", str(fecha_inicio) + "T01:00:00:00")
        marinaPlaylist.set("EndTime", str(fecha_fin_transformada) + "T00:59:59:24")
        properties = ET.SubElement(marinaPlaylist, "properties")
        eventlist = ET.SubElement(marinaPlaylist, "eventList")

        # En la siguiente iteración vamos a recorrer los eventos que hemos guardado en el diccionario de eventos, y vamos a crear dos variables, event para saber el numero de evento y
        # diccionario_interno para saber el diccionario que vamos a usar para crear el evento
        for event, diccionario_interno in eventos.items():

            # Si es tipo 4, vamos a seguir la siguiente logica para generar una rama XML de tipo 4
            if diccionario_interno['TIPOREG'] == "4":
                event4 = ET.SubElement(eventlist, "event")
                event4.set("type", "Comment")
                #event4.set("type", "BlockStart")
                properties4 = ET.SubElement(event4, "properties")
                #properties4.set("blockname", diccionario_interno["IDBLOQUE"].rstrip())
                schedule4 = ET.SubElement(properties4, "schedule")
                schedule4.set("startType", "Sequential")
                event4_1 = ET.SubElement(properties4, "event")
                comment4 = ET.SubElement(event4_1, "comment")
                comment4.text = "BLOQUE:"+" "+diccionario_interno["IDBLOQUE"].rstrip()
                # Creamos una variable con el ID del bloque que irá en cada SPOT del bloque
                bloque_publi = diccionario_interno["IDBLOQUE"].rstrip()

            # Si es tipo 5, vamos a seguir la siguiente logica para generar una rama XML de tipo 5
            if diccionario_interno['TIPOREG'] == "5":
                event5 = ET.SubElement(eventlist, "event")
                event5.set("type", "Comment")
                properties5 = ET.SubElement(event5, "properties")
                schedule5 = ET.SubElement(properties5, "schedule")
                schedule5.set("startType", "Sequential")
                event5_1 = ET.SubElement(properties5, "event")
                comment5 = ET.SubElement(event5_1, "comment")
                comment5.text = diccionario_interno["OBSERVACIONES"].rstrip()
            # Si tipo1
            # Si en este caso es tipo directo, o lo que es lo mismo, el valor del campo DIRGRAB es D seguimos la siguiente logica
            if diccionario_interno['TIPOREG'] == "1":
                if diccionario_interno['DIRGRAB'] == "D":
                    event1 = ET.SubElement(eventlist, "event")
                    event1.set("type", "Live")
                    properties1 = ET.SubElement(event1, "properties")
                    schedule1 = ET.SubElement(properties1, "schedule")
                    schedule1.set("endType", "Hold")
                    schedule1.set("endOffset", diccionario_interno['TIDUMINUT'])
                    media1 = ET.SubElement(properties1, "media")
                    media1.set("mediaType", "Live")
                    media1.set("mediaName", diccionario_interno["TICODELEMENMIN"].rstrip()),
                    # media1.set("mediaName", "TESTOK"),
                    switch1 = ET.SubElement(properties1, "switch")
                    source1 = ET.SubElement(switch1, "source")
                    source1.set("type", "Logical")
                    logical1 = ET.SubElement(source1, "logical")
                    logical1.set("name", diccionario_interno["TICODELEMENMIN"].rstrip())
                    destination1 = ET.SubElement(switch1, "destination")
                    destination1.set("type", "Auto")
                    auto1 = ET.SubElement(destination1, "auto")
                    auto1.set("type", "PGM")

                    if diccionario_interno['Tipo2']['NUMSEGMENTO'] != "0":
                        mediaStream1.set("som", diccionario_interno['Tipo2']["HORINIEMI"].rstrip())
                        schedule1.set("endOffset", diccionario_interno['Tipo2']['HORFINEMI'].rstrip())
                elif diccionario_interno['DIRGRAB'] == "G":
                    event1 = ET.SubElement(eventlist, "event")
                    event1.set("type", "PrimaryVideo")
                    properties1 = ET.SubElement(event1, "properties")
                    schedule1 = ET.SubElement(properties1, "schedule")
                    schedule1.set("endType", "Duration")
                    schedule1.set("endOffset", diccionario_interno['TIDUMINUT'])
                    media1 = ET.SubElement(properties1, "media")
                    media1.set("mediaType", "Video")
                    media1.set("mediaName", diccionario_interno["TICODELEMENMIN"].rstrip())
                    # media1.set("mediaName", "TESTOK"),
                    mediaStream1 = ET.SubElement(properties1, "mediaStream")
                    mediaStream1.set("som", diccionario_interno['Tipo2']["HORINIEMI"].rstrip())
                    video1 = ET.SubElement(mediaStream1, "video")
                    video1.set("jobType", "Play")
                    segment1 = ET.SubElement(mediaStream1, "segment")
                    segment1.set("type", "Media")
                    if diccionario_interno['Tipo2']['NUMSEGMENTO'] != "0":
                        segment1.set("type", "Markup")
                        markup1 =ET.SubElement(segment1,"markup")
                        markup1.set("orderNo",diccionario_interno['Tipo2']['NUMSEGMENTO'])
                        mediaStream1.set("som", diccionario_interno['Tipo2']["HORINIEMI"].rstrip())
                        schedule1.set("endOffset", diccionario_interno['Tipo2']['HORFINEMI'].rstrip())

                # Se agrega etiquetas comunes de ambos casos
                event1_2 = ET.SubElement(properties1, "event")
                event1_2.set("title", diccionario_interno["TITITELEME"].strip())
                event1_2.set("reconcileKey", diccionario_interno["RECONCILEKEY"])
                classifications1 = ET.SubElement(event1_2, "classifications")
                classification1 = ET.SubElement(classifications1, "classification")
                classification1.set("classification", "EventType")
                classification1.set("category", diccionario_interno["TITIPELEME"])
                mediaStream1 = ET.SubElement(properties1, "mediaStream")
                mediaStream1.set("som", diccionario_interno['Tipo2']["HORINIEMI"].rstrip())

                # Si es una publicidad le añadimos comentario con el nombre de bloque
                if diccionario_interno["TITIPELEME"] == "B":
                    comment1 = ET.SubElement(event1_2, "comment")
                    comment1.text = bloque_publi

                # Se comprueba si es tipo fijo o tipo secuencial
                if diccionario_interno['INDELEMFIJO'] == "F":
                    schedule1.set("startType", "Fixed")
                    schedule1.set("startOffset", fecha_inicio + "T" + diccionario_interno['TIHOINMIN'])
                else:
                    schedule1.set("startType", "Sequential")

                feature_1 = ET.SubElement(properties1, "features")
                # Se comprueba el modo de audio, que puede ser EST Estereo; DST Dual-Estereo; MON Mono; DUA Dual; DP1 Dolby PAR 1; DP2 Dolby PAR 2; DP3 Dolby PAR 3; DG1 Dolby DUAL DRUPO1; DG2 Dolby DUAL DRUPO2
                if diccionario_interno['TIPO_DE_AUDIO'] != "   ":


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
                    #feature_audio2 = ET.SubElement(features_audio, "feature")
                    #feature_audio2.set("type", "Subtitle")

                    # Crear un diccionario para mapear los valores de TIPO_DE_AUDIO a los nombres correspondientes
                    tipo_audio_names = {
                       # "EST": "ESTEREO",
                       # "DST": "Dual-Estereo",
                       # "MON": "MONO",
                       # "DUA": "DUAL",
                       # "DP1": "Dolby PAR 1",
                       # "DP2": "Dolby PAR 2",
                       # "DP3": "Dolby PAR 3",
                       # "DG1": "Dolby DUAL DRUPO1",
                       # "DG2": "Dolby DUAL DRUPO2"

                        "EST": "3-ST",
                        "DST": "2-DL-ST",
                        "MON": "1-MONO",
                        "DUA": "2-DL-ST-DOLBY",
                        "DP1": "7-DOLBY1",
                        "DP2": "8-DOLBY2",
                        "DP3": "Dolby PAR 3",
                        "DG1": "5-DUAL5-6",
                        "DG2": "6-DUAL3-4"

                    }

                    # Obtener el nombre correspondiente a TIPO_DE_AUDIO
                    nombre_audio = tipo_audio_names.get(diccionario_interno['TIPO_DE_AUDIO'])

                    # Crear el elemento trackPreset y establecer el atributo "name"
                    if nombre_audio:
                        trackpreset = ET.SubElement(audioshuffle, "trackPreset")
                        trackpreset.set("name", nombre_audio)

                # Se comrpueba si viene subtitulado o no, para ello usamos el campo llamado "SUBTITULADO", si es S vendra en castellano, si es I vendra en ingles y castellano y si viene en blanco no tiene subtitulos
                if diccionario_interno['SUBTITULADO'] == "S":
                    #features1 = ET.SubElement(properties1, "features")
                    #feature1 = ET.SubElement(features1, "feature")
                    feature2 = ET.SubElement(feature_1, "feature")
                    feature2.set("type", "Subtitle")
                    properties_feature = ET.SubElement(feature2, "properties")
                    mediaStream1_feature = ET.SubElement(properties_feature, "mediaStream")
                    mediaStream1_feature.set("som", "$INHERITS$")
                    subtitle = ET.SubElement(mediaStream1_feature, "subtitle")
                    subtitle.set("CaptionMode", "None")
                    language = ET.SubElement(subtitle, "languages")
                    lang = ET.SubElement(language, "lang")
                    lang.text = "ESP"
                    allocation = ET.SubElement(subtitle, "allocation")
                    allocation.set("type", "ListStream")
                    liststream = ET.SubElement(allocation, "listStream")
                    liststream.set("listStreamNo", "0")
                    liststream.set("type", "Fixed")
                    media_subtitle = ET.SubElement(mediaStream1_feature, "media")
                    media_subtitle.set("mediaType", "Subtitle")
                    media_subtitle.set("mediaName", "$INHERITS$")
                elif diccionario_interno['SUBTITULADO'] == "I":
                    #features1 = ET.SubElement(properties1, "features")
                    #feature1 = ET.SubElement(features1, "feature")
                    feature2 = ET.SubElement(feature_1, "feature")
                    feature2.set("type", "Subtitle")
                    properties_feature = ET.SubElement(feature2, "properties")
                    mediaStream1_feature = ET.SubElement(properties_feature, "mediaStream")
                    mediaStream1_feature.set("som", "$INHERITS$")
                    subtitle = ET.SubElement(mediaStream1_feature, "subtitle")
                    subtitle.set("CaptionMode", "None")
                    language = ET.SubElement(subtitle, "languages")
                    lang1 = ET.SubElement(language, "lang")
                    lang1.text = "ESP"
                    lang2 = ET.SubElement(language, "lang")
                    lang2.text = "ENG"
                    allocation = ET.SubElement(subtitle, "allocation")
                    allocation.set("type", "ListStream")
                    liststream = ET.SubElement(allocation, "listStream")
                    liststream.set("listStreamNo", "0")
                    liststream.set("type", "Fixed")
                    media_subtitle = ET.SubElement(mediaStream1_feature, "media")
                    media_subtitle.set("mediaType", "Subtitle")
                    media_subtitle.set("mediaName", "$INHERITS$")

                # Creamos una rama de XML para todos los tipo 1, si cumple la siguiente condición, esta ira rellena, si no, ira vacia
                child_event = ET.SubElement(event1, "childEvents")

                #A partir de aqui, creamos la condicion de que, si el campo TITIPELEME es A, D, E o P, se genera el branding
                if diccionario_interno["TITIPELEME"] in ["A","D","E","P"]:
                    # Las columnas de la tabla siguiente corresponde al Custom ID* | PT, SC or empty | NR7 | NR12 | NR16 |NR18 
                    tabla = {
                        'LA 1': ['L101', 'L106', 'L107', 'L112', 'L116', 'L118'],
                        'LA 2': ['L201', 'L206', 'L207', 'L212', 'L216', 'L218'],
                        'CANAL 24H': ['L401', 'L406', 'L407', 'L412', 'L416', 'L418'],
                        'TELEDEPORTE': ['L702', 'L706', 'L707', 'L712', 'L716', 'L718'],
                        'CLAN TVE': ['L501', 'L506', 'L507', 'L512', 'L516', 'L518'],
                        'Star TVE HD': ['L601', 'L606', 'L607', 'L612', 'L616', 'L618'],
                        'INTERNACIONALES': ['L301', 'L306', 'L307', 'L312', 'L316', 'L318']
                    }

                    # Logica que vamos a usar para determinar los canales que vienen a internacionales, que llevan nombre distintos
                    if LICADENA in ["TVE EUROPA-AFRICA", "TVE ASIA", "TVE AMERICA"]:
                        LICADENA ="INTERNACIONALES"

                    # Distintas decisiones dependiendo de la calificacion moral que tenga, nombramos la variable columna para poder recorrer la tabla
                    # Una vez dicidida la columna, vamos a buscar el nombre del grafico en la tabla correspondiente, usando la variable licadena que nos indica el nombre del canal, y con la columna que nos indica la calificacion moral                   
                    # Guardar el resultado de rstrip() en una variable
                    califmoral_stripped = diccionario_interno["CALIFMORAL"].rstrip()

                    # Mapeo de CALIFMORAL a columnas
                    califmoral_to_column = {
                        "PT": 1,
                        "": 1,
                        "SC": 1,
                        "NR7": 2,
                        "NR12": 3,
                        "NR16": 4,
                        "NR18": 5
                    }

                    # Determinar la columna basada en CALIFMORAL
                    columna = califmoral_to_column.get(califmoral_stripped, 0)

                    # Determinar el logo_branding
                    if columna == 0:
                        for prefix in media_id_espciales:
                            if diccionario_interno["TICODELEMENMIN"].startswith(prefix):
                                logo_branding = tabla[LICADENA][0]
                                break
                    else:
                        logo_branding = tabla[LICADENA][columna]

                    # Generamos el arbol xml que va a colgar de childevents
                    event_child_1 = ET.SubElement(child_event, "event")
                    event_child_1.set("type", "VizRT")

                    # Añadir el elemento 'properties' dentro de 'event'
                    properties_child = ET.SubElement(event_child_1, "properties")

                    # Añadir el elemento 'schedule' dentro de 'properties'
                    schedule_child = ET.SubElement(properties_child, "schedule")
                    schedule_child.set("endType", "-ParentEnd")
                    schedule_child.set("startType", "+ParentStart")
                    schedule_child.set("endOffset", "00:00:00:00")
                    schedule_child.set("startOffset", "00:00:00:00")

                    # Añadir el elemento 'mediaStream' dentro de 'properties'
                    mediaStream_child = ET.SubElement(properties_child, "mediaStream")

                    # Añadir los elementos 'cg' y 'allocation' dentro de 'mediaStream'
                    cg = ET.SubElement(mediaStream_child, "cg")
                    cg.set("layer", "0")
                    cg.set("type", "Page")

                    # Añadir el elemento 'media' dentro de 'properties'
                    media_child = ET.SubElement(properties_child, "media")
                    media_child.set("mediaType", "CG")
                    media_child.set("mediaName", logo_branding)


                # Agregamos la logica oara poder sacar el valor del grafico secundario, usando el diccionario interno y las variables del tipo de audio, subtitulado y audiodescripcion

                grafico_secundario = ""
                if diccionario_interno["TIPO_DE_AUDIO"] in ["DST","DUA"]: 
                    if diccionario_interno["SUBTITULADO"] == " ":
                        if diccionario_interno["AUDIODESCRIPCION"] == " ":
                            grafico_secundario = "V011"
                        else:
                            grafico_secundario = "V016"
                    else:
                        if diccionario_interno["AUDIODESCRIPCION"] == " ":
                            grafico_secundario = "V013"
                        else:
                            grafico_secundario = "V017"
                elif diccionario_interno["TIPO_DE_AUDIO"] in ["DP2","DP1","DP3"]:
                    if diccionario_interno["SUBTITULADO"] == " ":
                        if diccionario_interno["AUDIODESCRIPCION"] == " ":
                            grafico_secundario = "V030"
                        else:
                            grafico_secundario = "V034"
                    else:
                        if diccionario_interno["AUDIODESCRIPCION"] == " ":
                            grafico_secundario = "V032"
                        else:  
                            grafico_secundario = "V035"
                elif diccionario_interno["TIPO_DE_AUDIO"] in ["DG1","DG2"]:
                    if diccionario_interno["SUBTITULADO"] == " ":
                        if diccionario_interno["AUDIODESCRIPCION"] == " ":
                            grafico_secundario = "V031"
                        else:
                            grafico_secundario = "V036"
                    else:
                        if diccionario_interno["AUDIODESCRIPCION"] == " ":
                            grafico_secundario = "V033"
                        else:
                            grafico_secundario = "V037"
                else:
                    if diccionario_interno["SUBTITULADO"] == " ":
                        if diccionario_interno["AUDIODESCRIPCION"] != " ":
                            grafico_secundario = "V014"
                    else:
                        if diccionario_interno["AUDIODESCRIPCION"] != " ":
                            grafico_secundario = "V012"
                        else:
                            grafico_secundario = "V015"

                if grafico_secundario != "":

                    # Generamos el arbol xml que va a colgar de childevents
                    event_child_2 = ET.SubElement(child_event, "event")
                    event_child_2.set("type", "VizRT")

                    # Añadir el elemento 'properties' dentro de 'event'
                    properties_child = ET.SubElement(event_child_2, "properties")

                    # Añadir el elemento 'schedule' dentro de 'properties'
                    schedule_child = ET.SubElement(properties_child, "schedule")
                    schedule_child.set("endType", "-ParentEnd")
                    schedule_child.set("startType", "+ParentStart")
                    schedule_child.set("endOffset", "00:00:00:00")
                    schedule_child.set("startOffset", "00:00:00:00")
                    # Añadir el elemento 'mediaStream' dentro de 'properties'
                    mediaStream_child = ET.SubElement(properties_child, "mediaStream")

                    # Añadir los elementos 'cg' y 'allocation' dentro de 'mediaStream'
                    cg = ET.SubElement(mediaStream_child, "cg")
                    cg.set("layer", "0")
                    cg.set("type", "Page")

                    # Añadir el elemento 'media' dentro de 'properties'
                    media_child = ET.SubElement(properties_child, "media")
                    media_child.set("mediaType", "CG")
                    media_child.set("mediaName", grafico_secundario)

                # Recorremos los diccionarios de tipo 3:
                for clave, diccionario_tipo_3 in diccionario_interno.items():
                    if clave.startswith('Tipo3_'):
                        grafico_tipo3 = diccionario_tipo_3["NUMERO_DE_LA_INCRUSTACION"]
                        # Generamos el arbol xml que va a colgar de childevents
                        event_child_5 = ET.SubElement(child_event, "event")
                        event_child_5.set("type", "VizRT")

                        # Añadir el elemento 'properties' dentro de 'event'
                        properties_child_5 = ET.SubElement(event_child_5, "properties")

                        # Añadir el elemento 'schedule' dentro de 'properties'
                        schedule_child_5 = ET.SubElement(properties_child_5, "schedule")

                        # Si la hora de comienzo es T (duración total)
                        if diccionario_tipo_3["HORA_DE_COMIENZO"].strip() == "T":
                            schedule_child_5.set("endType", "-ParentEnd")
                            schedule_child_5.set("startType", "+ParentStart")
                            schedule_child_5.set("endOffset", "00:00:00:00")
                            schedule_child_5.set("startOffset", "00:00:00:00")

                        else:

                            schedule_child_5.set("startType", "+ParentStart")
                            schedule_child_5.set("startOffset", diccionario_tipo_3["HORA_DE_COMIENZO"])

                            # Si no tiene duración suponemos que es hasta final de evento principal
                            if diccionario_tipo_3["DURACION"].strip() == "":
                                schedule_child_5.set("endType", "-ParentEnd")
                                schedule_child_5.set("endOffset", "00:00:00:00")

                            # Si no, ponemos la duración
                            else:
                                schedule_child_5.set("endType", "Duration")
                                schedule_child_5.set("endOffset", diccionario_tipo_3["DURACION"])

                        # Añadir el elemento 'mediaStream' dentro de 'properties'
                        mediaStream_child_5 = ET.SubElement(properties_child_5, "mediaStream")

                        # Añadir los elementos 'cg' y 'allocation' dentro de 'mediaStream'
                        cg_5 = ET.SubElement(mediaStream_child_5, "cg")
                        cg_5.set("layer", "0")
                        cg_5.set("type", "Page")

                        # Añadir el elemento 'media' dentro de 'properties'
                        media_child_5 = ET.SubElement(properties_child_5, "media")
                        media_child_5.set("mediaType", "CG")
                        media_child_5.set("mediaName", diccionario_tipo_3["NUMERO_DE_LA_INCRUSTACION"])

        # Crear el objeto ElementTree para representar la estructura del XML
        tree = ET.ElementTree(marinaPlaylist)
        #print(marinaPlaylist)

        nombre_fichero_sin_extension = os.path.splitext(os.path.basename(archivo))[0]

        with open(directorio_salida+"/"+nombre_fichero_sin_extension+".mpl", "w", encoding="utf-8") as xml_file:
            # Obtener una representación en cadena de texto del XML y formatear el XML
            xml_str = ET.tostring(marinaPlaylist, encoding="utf-8")
            xml_formatted = xml.dom.minidom.parseString(xml_str).toprettyxml()

            # Escribir el XML formateado en el archivo
            xml_file.write(xml_formatted)
            print("XML generado exitosamente.")

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Este código define un método on_created que se llama cuando se crea un fichero. Si el elemento creado es un directorio, no devuelve nada y no se llama a ninguna funcion adicional. 
        Si el elemento creado es un archivo .trf o .TRF (Es sensible a las mayusculas), llama a una función procesar_archivo con la ruta del archivo creado como argumento.
        """
        if event.is_directory:
            return
        if event.src_path.endswith('.TRF') or event.src_path.endswith('.trf'):
            procesar_archivo(event.src_path)

def iniciar_monitoreo():
    """
    Este código define una función llamada iniciar_monitoreo que comienza a monitorear un directorio especificado en busca de cambios en los archivos usando las clases Observer y FileHandler de la librería watchdog. 
    Cuando la función es llamada, comienza a monitorizar el directorio especificado recursivamente, imprime un mensaje indicando que el directorio está siendo monitorizado, 
    y entonces entra en un bucle para dormir continuamente y comprobar si hay interrupciones de teclado para detener el proceso de monitorización.
    """

    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, directorio_a_monitorear, recursive=True)
    observer.start()
    print("Monitoreando el directorio:", directorio_a_monitorear)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# Este fragmento de código comprueba si el script actual se está ejecutando como programa principal, y si es así, llama a la función iniciar_monitoreo().
if __name__ == "__main__":
    iniciar_monitoreo()
