from pathlib import Path
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import datetime
from datetime import timedelta, datetime
import time
import logging
import sys
import ctypes
import configparser
import ftplib
import socket
def procesar_archivo(archivo, directorio_salida, origen_fichero):
    """
    Este fragmento de código Python define una función procesar_archivo que procesa un archivo, en este caso seran ficheros .trf. Extrae información del archivo de entrada, manipula los datos y escribe la salida formateada en un nuevo archivo. 
    El código incluye operaciones como la lectura de líneas específicas, la extracción de subcadenas y la escritura de datos formateados en un archivo de salida. 
    También registra el nombre del fichero procesado e imprime un mensaje en la consola.
    """
    config = configparser.ConfigParser()

    # Leer el archivo de configuración
    config.read(r'D:\Traductor\Ejecutor\cf\config.conf')
    #config.read(r'cf\config.conf')
    #config.read(r'C:\Users\franciscojavier.mart\Documents\parseo\programas\Ejecutor\cf\config.conf')

    # Obtener los valores de la sección Variables
    variables = config['variables']

    # Leer las variables especiales
    media_id_especiales = eval(variables['media_id_espciales'])  # Utilizando eval para interpretar la lista como una lista de Python
    tipo_audio_names = eval(variables['tipo_audio_names'])  # Utilizando eval para interpretar el diccionario como un diccionario de Python
    tabla = eval(variables['tabla'])  # Utilizando eval para interpretar el diccionario como un diccionario de Python
    califmoral_to_column = eval(variables['califmoral_to_column'])  # Utilizando eval para interpretar el diccionario como un diccionario de Python
    tipos_de_eventos = eval(variables['tipos_de_eventos'])

    # El log se genera si o si, si no existe la salida_log, se obvia

    nombre_archivo = os.path.basename(archivo)

    # Generamos el nombre del fichero para el log, eliminamos la ruta absoluta y nos quedamos solo con el nombre del fichero

    if origen_fichero:
        logging.info(f"Archivo procesado: {nombre_archivo} --> Destino del fichero: {directorio_salida}\MANUAL")
    else:
        logging.info(f"Archivo procesado: {nombre_archivo} --> Destino del fichero: {directorio_salida}\FTP")

    # Generamos el nombre del fichero para el log, eliminamos la ruta absoluta y nos quedamos solo con el nombre del fichero
    print("Procesando archivo:", archivo)

    #with open(archivo, "r", encoding="utf-8") as fichero:
    with open(archivo, "r", encoding="iso-8859-1") as fichero:

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
                    # Determinamos si es tipo Desconexión, si lo es, agregamos el comentario
                    if diccionario_interno['TITIPELEME'] == "D":
                        # Se insertan comentarios de desconexion
                        event1_comentario = ET.SubElement(eventlist, "event")
                        event1_comentario.set("type", "Comment")
                        properties1 = ET.SubElement(event1_comentario, "properties")
                        schedule1_comentario = ET.SubElement(properties1, "schedule")
                        schedule1_comentario.set("startType", "Sequential")
                        event1_comentario_1 = ET.SubElement(properties1, "event")
                        comment1 = ET.SubElement(event1_comentario_1, "comment")
                        comment1.text = "Desconexion con "+LICADENA
                    # Se genera el evento Live
                    event1 = ET.SubElement(eventlist, "event")
                    event1.set("type", "Live")
                    properties1 = ET.SubElement(event1, "properties")
                    schedule1 = ET.SubElement(properties1, "schedule")
                    schedule1.set("endType", "Hold")
                    schedule1.set("endOffset", diccionario_interno['TIDUMINUT'])
                    #media1 = ET.SubElement(properties1, "media")
                    #media1.set("mediaType", "Live")
                    #media1.set("mediaName", diccionario_interno["TICODELEMENMIN"].rstrip()),
                    # Aqui ponemos el enrutado de los directos que tienen como fuente el mismo mediaid del evento
                    switch1 = ET.SubElement(properties1, "switch")
                    source1 = ET.SubElement(switch1, "source")
                    source1.set("type", "Logical")
                    logical1 = ET.SubElement(source1, "logical")
                    logical1.set("name", diccionario_interno["TICODELEMENMIN"].rstrip())
                    # El destino lo estamos suponiendo como auto-PGM
                    destination1 = ET.SubElement(switch1, "destination")
                    destination1.set("type", "Auto")
                    auto1 = ET.SubElement(destination1, "auto")
                    auto1.set("type", "PGM")

                    #if diccionario_interno['Tipo2']['NUMSEGMENTO'] != "0":
                    #    mediaStream1.set("som", diccionario_interno['Tipo2']["HORINIEMI"].rstrip())
                    #    schedule1.set("endOffset", diccionario_interno['Tipo2']['HORFINEMI'].rstrip())
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
                classification1.set("category", tipos_de_eventos.get(diccionario_interno["TITIPELEME"]))
                schedule1.set("startType", "Sequential")
                #mediaStream1 = ET.SubElement(properties1, "mediaStream")
                #mediaStream1.set("som", diccionario_interno['Tipo2']["HORINIEMI"].rstrip())

                # Si es una publicidad le añadimos comentario con el nombre de bloque
                if diccionario_interno["TITIPELEME"] == "B":
                    comment1 = ET.SubElement(event1_2, "comment")
                    comment1.text = bloque_publi
                    media1.set("mediaName", "B" + diccionario_interno["CODLOCALI"].rstrip()+ diccionario_interno["NO_PA"].rstrip())

                # Se comprueba si es tipo fijo o tipo secuencial
                #if diccionario_interno['INDELEMFIJO'] == "F":
                #    schedule1.set("startType", "Fixed")
                #    schedule1.set("startOffset", fecha_inicio + "T" + diccionario_interno['TIHOINMIN'])
                #else:
                #    schedule1.set("startType", "Sequential")

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

                    # Obtener el nombre correspondiente a TIPO_DE_AUDIO
                    nombre_audio = tipo_audio_names.get(diccionario_interno['TIPO_DE_AUDIO'])

                    # Crear el elemento trackPreset y establecer el atributo "name"
                    if nombre_audio:
                        trackpreset = ET.SubElement(audioshuffle, "trackPreset")
                        trackpreset.set("name", nombre_audio)

                # Se comrpueba si viene subtitulado o no, para ello usamos el campo llamado "SUBTITULADO", si es S vendra en castellano, si es I vendra en ingles y castellano y si viene en blanco no tiene subtitulos
                if diccionario_interno['SUBTITULADO'] == "S" or diccionario_interno['SUBTITULADO'] == "I":
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
                    media_subtitle.set("mediaName", diccionario_interno["TICODELEMENMIN"].rstrip())
                #elif diccionario_interno['SUBTITULADO'] == "I":
                #    feature2 = ET.SubElement(feature_1, "feature")
                #    feature2.set("type", "Subtitle")
                #    properties_feature = ET.SubElement(feature2, "properties")
                #    mediaStream1_feature = ET.SubElement(properties_feature, "mediaStream")
                #    mediaStream1_feature.set("som", "$INHERITS$")
                #    subtitle = ET.SubElement(mediaStream1_feature, "subtitle")
                #    subtitle.set("CaptionMode", "None")
                #    language = ET.SubElement(subtitle, "languages")
                #    lang1 = ET.SubElement(language, "lang")
                #    lang1.text = "ESP"
                #    lang2 = ET.SubElement(language, "lang")
                #    lang2.text = "ENG"
                #    allocation = ET.SubElement(subtitle, "allocation")
                #    allocation.set("type", "ListStream")
                #    liststream = ET.SubElement(allocation, "listStream")
                #    liststream.set("listStreamNo", "0")
                #    liststream.set("type", "Fixed")
                #    media_subtitle = ET.SubElement(mediaStream1_feature, "media")
                #    media_subtitle.set("mediaType", "Subtitle")
                #    media_subtitle.set("mediaName", "$INHERITS$")


                # Agregadas lineas para generar las gpi de desconexiones, solo necesitamos que sea 
                if diccionario_interno["TITIPELEME"] in ["D"]:
                    feature_gpi = ET.SubElement(feature_1, "feature")
                    feature_gpi.set("type", "Macro")
                    properties_gpi = ET.SubElement(feature_gpi, "properties")
                    macro_gpi = ET.SubElement(properties_gpi, "macro")
                    macro_gpi.set("name", "GPI")

                # Creamos una rama de XML para todos los tipo 1, si cumple la siguiente condición, esta ira rellena, si no, ira vacia
                child_event = ET.SubElement(event1, "childEvents")

                #A partir de aqui, creamos la condicion de que, si el campo TITIPELEME es A, D, E o P, se genera el branding
                if diccionario_interno["TITIPELEME"] in ["A", "E", "P"]:

                    # Logica que vamos a usar para determinar los canales que vienen a internacionales, que llevan nombre distintos
                    if LICADENA in ["TVE EUROPA-AFRICA", "TVE ASIA", "TVE AMERICA"]:
                        LICADENA ="INTERNACIONALES"

                    # Distintas decisiones dependiendo de la calificacion moral que tenga, nombramos la variable columna para poder recorrer la tabla
                    # Una vez dicidida la columna, vamos a buscar el nombre del grafico en la tabla correspondiente, usando la variable licadena que nos indica el nombre del canal, y con la columna que nos indica la calificacion moral                   
                    # Guardar el resultado de rstrip() en una variable
                    califmoral_stripped = diccionario_interno["CALIFMORAL"].rstrip()

                    # Determinar la columna basada en CALIFMORAL
                    columna = califmoral_to_column.get(califmoral_stripped, 0)

                    # Determinar el logo_branding
                    if columna == 0:
                        for prefix in media_id_especiales:
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


                # Agregamos la logica para poder sacar el valor del grafico secundario, usando el diccionario interno y las variables del tipo de audio, subtitulado y audiodescripcion

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
                    cg.set("layer", "1")
                    cg.set("type", "Page")

                    # Añadir el elemento 'media' dentro de 'properties'
                    media_child = ET.SubElement(properties_child, "media")
                    media_child.set("mediaType", "CG")
                    media_child.set("mediaName", grafico_secundario)

                # Recorremos los diccionarios de tipo 3:
                # Contador para el tipo de grafico
                contador_viz = 2
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
                            schedule_child_5.set("startOffset", diccionario_tipo_3["HORA_DE_COMIENZO"].strip())

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
                        # Se cambia el tipo de elemento a tipo str oara evitar errores
                        cg_5.set("layer", str(contador_viz))
                        cg_5.set("type", "Page")

                        # Añadir el elemento 'media' dentro de 'properties'
                        media_child_5 = ET.SubElement(properties_child_5, "media")
                        media_child_5.set("mediaType", "CG")
                        media_child_5.set("mediaName", diccionario_tipo_3["NUMERO_DE_LA_INCRUSTACION"])

                        # Añadir el comentario con el tipo de inserción
                        media_child_6 =ET.SubElement(media_child_5, "event")
                        comment5 = ET.SubElement(media_child_6, "comment")
                        comment5.text = diccionario_tipo_3["TIPO_DE_INSERCION"]

                        # Incrementamos el contador de la capa
                        contador_viz += 1


        # Crear el objeto ElementTree para representar la estructura del XML
        tree = ET.ElementTree(marinaPlaylist)
        #print(marinaPlaylist)

        nombre_fichero_sin_extension = os.path.splitext(os.path.basename(archivo))[0]

        with open(directorio_salida+"/"+nombre_fichero_sin_extension+".mpl", "w", encoding="utf-8") as xml_file:
            # Obtener una representación en cadena de texto del XML y formatear el XML
            xml_str = ET.tostring(marinaPlaylist, encoding="iso-8859-1")
            xml_formatted = xml.dom.minidom.parseString(xml_str).toprettyxml()

            # Escribir el XML formateado en el archivo
            xml_file.write(xml_formatted)
            print("XML generado exitosamente.")

def descargar_archivos():
    """
    Descarga archivos desde un servidor FTP, utilizando la información de un archivo de configuración.
    """    

    # Crear un objeto ConfigParser para leer el archivo de configuración
    config = configparser.ConfigParser()

    # Leer el archivo de configuración y obtener los datos
    try:
        config.read(r'D:\Traductor\Ejecutor\cf\config.conf')
        #config.read(r'cf\config.conf')
        #config.read(r'C:\Users\franciscojavier.mart\Documents\parseo\programas\Ejecutor\cf\config.conf')
    except (IOError, configparser.Error) as e:
        logging.error("Error al leer el archivo de configuración:", e)
        return

    ## Configurar el ficehero de log
    datos_log = config['logs']
    ruta_log = datos_log.get('ruta_log')
    logging.basicConfig(filename=ruta_log +'\\'+'registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Leer datos de FTP de la sección 'datos_ftp'
    try:
        datos_ftp = config['datos_ftp']
        if not datos_ftp:
            logging.error("datos_ftp es None")
            return

        host = datos_ftp.get('ip_ftp')
        if not host:
            logging.error("El parametro ip_ftp del fichero de configuración esta vacio")
            return

        usuario = datos_ftp.get('usuario_ftp')
        if not usuario:
            logging.error("El parametro usuario_ftp del fichero de configuración esta vacio")
            return

        contraseña = datos_ftp.get('pass_ftp')
        if not contraseña:
            logging.error("El parametro pass_ftp del fichero de configuración esta vacio")
            return

        directorio_descarga_ficheros = datos_ftp.get('ruta_ficheros')
        if directorio_descarga_ficheros is None:
            logging.error("El valor de la clave 'ruta_ficheros' en el archivo de configuración es None")
            return

        try:
            Path(directorio_descarga_ficheros).resolve(strict=True)
        except FileNotFoundError:
            logging.error("Directorio de descarga de ficheros no existe, revise la configuración")
            return

        directorio_salida_ficheros = datos_ftp.get('ruta_destino')
        if directorio_salida_ficheros is None:
            logging.error("El valor de la clave 'ruta_destino' en el archivo de configuración es None")
            return

        try:
            Path(directorio_salida_ficheros).resolve(strict=True)
        except FileNotFoundError:
            logging.error("Directorio de salida de ficheros no existe, revise la configuración")
            return


    except KeyError:
        logging.error("No se ha encontrado la sección 'datos_ftp' en el archivo de configuración, Revisar Ruta del archivo de configuración.")
        return

    directorio_descargar_ftp = datos_ftp.get('directorio_descarga_ftp')
    

    # Leer datos de descarga de archivos de la sección 'descarga_archivos' si existe, si no existe, se sustituye por la ruta predeterminada
    if not directorio_descargar_ftp or directorio_descargar_ftp == '':
        directorio_descargar_ftp = '/'

    # Crear una lista para almacenar los nombres de los archivos descargados
    archivos_descargados = []

    # Conexión al servidor FTP y descarga los archivos
    try:
        ftp = ftplib.FTP(host)
    except (OSError, socket.error):
        logging.error("Error al conectarse al servidor FTP: %s", host)
        return
    try:
        ftp.login(usuario, contraseña)
    except ftplib.error_perm:
        logging.error("Error al iniciar sesión en el servidor FTP, credenciales incorrectas")
        ftp.quit()
        return

    # Cambiar el directorio de trabajo
    try:
        if directorio_descargar_ftp != '':
            ftp.cwd(directorio_descargar_ftp)
    except ftplib.error_perm:
        logging.error("Error al cambiar el directorio de trabajo: El diretorio no es correcto o no se tienen permisos suficientes")

    # Obtener lista de archivos en el directorio actual del servidor
    try:
        archivos_ftp = ftp.nlst()
    except ftplib.error_temp:
        logging.error("Error al obtener la lista de archivos del servidor FTP")
        ftp.quit()
        return
    # Obtener la fecha de hoy
    hoy = datetime.now().date()

    # Iterar sobre los archivos y descargar los del día de hoy y que empiecen por un prefijo
    datos_fichero = eval(datos_ftp['tipo_fichero'])

    for archivo_ftp in archivos_ftp:
        if archivo_ftp.endswith('.trf') or archivo_ftp.endswith('.TRF') and archivo_ftp[:2] in datos_fichero:
        # Obtener la fecha de modificación del archivo
            try:
                fecha_modificacion = datetime.strptime(ftp.sendcmd('MDTM ' + archivo_ftp)[4:], "%Y%m%d%H%M%S").date()
            except ValueError:
                logging.error("Error al obtener la fecha de modificación del archivo", archivo_ftp)
                continue
            
            # Comparar la fecha de modificación con la fecha de hoy
            if fecha_modificacion == hoy:
                try:
                    # Crear una carpeta llamada "FTP" si no existe
                    directorio_ftp = directorio_descarga_ficheros + '/FTP'
                    if not os.path.exists(directorio_ftp):
                        os.makedirs(directorio_ftp)
                    # Descargamos el archivo  
                    with open(directorio_ftp + "/" + archivo_ftp, 'wb') as f:
                        ftp.retrbinary('RETR ' + archivo_ftp, f.write)
                except (OSError, IOError):
                    logging.error("Error al descargar el archivo", archivo_ftp)
                    continue
                ruta_fichero = directorio_ftp + '/' + archivo_ftp
                procesar_archivo(ruta_fichero, directorio_salida_ficheros, False)
    
                archivos_descargados.append(archivo_ftp)

    # Cerrar la conexión FTP
    ftp.quit()

    # comprobamos si hay ficheros en el directorio manual si existe, si no, lo creamos
    try:
        directorio_manual = directorio_descarga_ficheros + '/MANUAL'
        if not os.path.exists(directorio_manual):
            os.makedirs(directorio_manual)
    except (OSError, IOError):
        logging.error("Error al crear el directorio MANUAL")
    
    # Listamos los ficheros que hay dentro del directorio MANUAL, si hay ficheros se procesan, si no, no se hace nada.
    archivos_manuales_procesados = []
    try:
        """
        Si existe el directorio MANUAL, leemos todos los ficheros que haya dentro y
        los procesamos si cumplen con las condiciones de extensión y de que el código
        de fichero sea uno de los que se permiten
        """
        if os.path.exists(directorio_manual):
            archivos_manual = os.listdir(directorio_manual)
            for archivo_manual in archivos_manual:
                """
                El fichero es válido si cumple con las condiciones de extensión y de
                que el código de fichero sea uno de los que se permiten
                """
                if archivo_manual.endswith('.trf') or archivo_manual.endswith('.TRF') and archivo_manual[:2] in datos_fichero:
                    """
                    Obtenemos la fecha de modificación del archivo en crudo y la
                    convertimos a legible
                    """
                    try:
                        fecha_modificacion = os.path.getmtime(directorio_manual + '/' + archivo_manual)
                        fecha_modificacion_legible = datetime.fromtimestamp(fecha_modificacion).date()
                    except (ValueError, FileNotFoundError) as e:
                        logging.error("Error al obtener la fecha de modificación del archivo %s: %s", archivo_manual, e)
                        continue
                    """
                    Obtenemos la fecha de hoy para compararlo con el fichero que
                    estamos tratando, si el fichero tiene fecha de hoy se trata,
                    si no no
                    """
                    hoy = datetime.now().date()
                    if fecha_modificacion_legible == hoy:
                        archivos_manuales_procesados.append(archivo_manual)
                        ruta_fichero = directorio_manual + '/' + archivo_manual
                        procesar_archivo(ruta_fichero, directorio_salida_ficheros, True)

    except (OSError, IOError):
        logging.error("Error al descargar el archivo de forma manual %s", archivo_manual)

    # Agregada la verificación de que se descargaron los archivos
    if not archivos_descargados and not archivos_manuales_procesados:
        logging.info("No se han descargado archivos del FTP y no se han procesado ficheros de MANUAL")

    elif not archivos_descargados and archivos_manuales_procesados:
        logging.info("Archivos manuales procesados correctamente: %s", archivos_manuales_procesados)

    elif archivos_descargados and not archivos_manuales_procesados:
        logging.info("Archivos descargados correctamente: %s", archivos_descargados)

    else:
        logging.info("Archivos descargados correctamente: %s y archivos manuales procesados correctamente: %s", archivos_descargados, archivos_manuales_procesados)

descargar_archivos()







