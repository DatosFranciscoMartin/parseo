import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import datetime
from datetime import timedelta, datetime
import tkinter as tk
from tkinter import filedialog
import logging

media_id_espciales = ["P0*","P3*","A5*","P4*","P5*","P611PDS00049*","P699EDS00006*","P699EGS00121*","P611PGS00595*","P699PGS00568*","P699PGS00872*","P611PGS00547*","P899PGS00064*","P211PDS00033*","P211PDS00034*","P699PGS00961*","P211PDS00036*","P211EGS00006*","P531PGS00057*","P531PGS00056*","P211EGS00007*","P211PDS00037*","P211EGS00008*","P463PGS00057*","P211EGS00009*","P211PDS00038*","P469PDS00102*"]

def seleccionar_directorio_salida():
    """
    Pide al usuario que seleccione un directorio y almacena el directorio seleccionado en la variable global 'directorio_salida'.
    Si se selecciona un directorio, actualiza el texto de la etiqueta 'etiqueta_directorio_salida' para mostrar el directorio seleccionado.
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
    archivos = filedialog.askopenfilenames(filetypes=(("Archivos TRF", "*.TRF"), ("Todos los archivos", "*.*")))

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

log_file = os.path.join(directorio_salida, "log.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M')

for archivo in lista_archivos:
    #fichero = open(archivo, "r", encoding="utf-8")
    fichero = open(archivo, "r") #le he quitado encoding="utf-8"
    nombre_archivo = os.path.basename(archivo)
    logging.info(f"Archivo procesado: {nombre_archivo}")

    # Sacamos el nombre del fichero en el cual tenemos información acerca de la fecha y hora de creación
    #nombre_archivo = os.path.basename(archivo)

    # La fecha de inicio la sacamos de la siguiente forma sobre el nombre del fichero
    #fecha_inicio = "20" + nombre_archivo[2:4] + "-" + nombre_archivo[4:6] + "-" + nombre_archivo[6:8]

    # Transformamos la fecha de inicio a un objeto de tipo datetime
    #fecha_transformada = datetime.strptime(fecha_inicio, "%Y-%m-%d")

    # Sumamos un dia a la fecha ya transformada
    #fecha_fin = fecha_transformada + timedelta(days=1)

    # Transformamos la fecha de fin a una cadena de texto para usarla mas adelante
    #fecha_fin_transformada = fecha_fin.strftime("%Y-%m-%d")

    # Nos saltamos la primera linea del fichero y sacamos sus datos.
    primera_linea = fichero.readline()

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
            RECONCILEKEY = CLASIFICACION + RELACION_DE_ASPECTO + TXTAUD + TITIPELEME + CONTRATO + PASE + TICODELEMENMIN[
                                                                                                         :11] + TICODELEMENMIN[
                                                                                                                11:13] + "_" + TIHOINMIN[
                                                                                                                               :8]
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
                "HORA_DE_COMIENZO": linea[8:19],
                "DURACION": linea[20:31]
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

    for event, diccionario_interno in eventos.items():
        print(diccionario_interno)

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

            # Se comprueba si es tipo fijo o tipo secuencial
            if diccionario_interno['INDELEMFIJO'] == "F":
                schedule1.set("startType", "Fixed")
                schedule1.set("startOffset", fecha_inicio + "T" + diccionario_interno['TIHOINMIN'])
            else:
                schedule1.set("startType", "Sequential")

            # Se comprueba el modo de audio, que puede ser EST Estereo; DST Dual-Estereo; MON Mono; DUA Dual; DP1 Dolby PAR 1; DP2 Dolby PAR 2; DP3 Dolby PAR 3; DG1 Dolby DUAL DRUPO1; DG2 Dolby DUAL DRUPO2

            if diccionario_interno['TIPO_DE_AUDIO'] != "   ":

                features_audio = ET.SubElement(properties1, "features")
                feature_audio1 = ET.SubElement(features_audio, "feature")
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
                audioshaffle = ET.SubElement(effect_feature_audio, "audioShuffle")
                audioshaffle.set("type", "TrackPreset")
                feature_audio2 = ET.SubElement(features_audio, "feature")
                feature_audio2.set("type", "Subtitle")
                    
                if diccionario_interno['TIPO_DE_AUDIO'] == "EST":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "ESTEREO")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "DST":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "Dual-Estereo")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "MON":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "MONO")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "DUA":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "DUAL")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "DP1":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "Dolby PAR 1")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "DP2":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "Dolby PAR 2")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "DP3":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "Dolby PAR 3")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "DG1":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "Dolby DUAL DRUPO1")
                elif diccionario_interno['TIPO_DE_AUDIO'] == "DG2":
                    trackpreset = ET.SubElement(audioshaffle, "trackPreset")
                    trackpreset.set("name", "Dolby DUAL DRUPO2")



            # Se comrpueba si viene subtitulado o no, para ello usamos el campo llamado "SUBTITULADO", si es S vendra en castellano, si es I vendra en ingles y castellano y si viene en blanco no tiene subtitulos
            if diccionario_interno['SUBTITULADO'] == "S":
                features1 = ET.SubElement(properties1, "features")
                feature1 = ET.SubElement(features1, "feature")
                feature2 = ET.SubElement(features1, "feature")
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
                features1 = ET.SubElement(properties1, "features")
                feature1 = ET.SubElement(features1, "feature")
                feature2 = ET.SubElement(features1, "feature")
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
                    '24H': ['L401', 'L406', 'L407', 'L412', 'L416', 'L418'],
                    'TDP': ['L702', 'L706', 'L707', 'L712', 'L716', 'L718'],
                    'CLAN': ['L501', 'L506', 'L507', 'L512', 'L516', 'L518'],
                    'STAR': ['L601', 'L606', 'L607', 'L612', 'L616', 'L618'],
                    'INTERNACIONALES': ['L301', 'L306', 'L307', 'L312', 'L316', 'L318']
                }

                # Distintas decisiones dependiendo de la calificacion moral que tenga, nombramos la variable columna para poder recorrer la tabla
                if diccionario_interno["TICODELEMENMIN"] in media_id_espciales:
                    columna = 0
                elif diccionario_interno["CALIFMORAL"].rstrip() in ["PT","","SC"]:
                    columna = 1
                elif diccionario_interno["CALIFMORAL"].rstrip() == "NR7":
                    columna = 2
                elif diccionario_interno["CALIFMORAL"].rstrip() == "NR12":
                    columna = 3
                elif diccionario_interno["CALIFMORAL"].rstrip() == "NR16":
                    columna = 4
                elif diccionario_interno["CALIFMORAL"].rstrip() == "NR18":
                    columna = 5
                
                # Una vez dicidida la columna, vamos a buscar el nombre del grafico en la tabla correspondiente, usando la variable licadena que nos indica el nombre del canal, y con la columna que nos indica la calificacion moral
                logo_branding = tabla[LICADENA][columna]

                # Generamos el arbol xml que va a colgar de childevents
                event_child_1 = ET.SubElement(child_event, "event")
                event_child_1.set("type", "CG")

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

            # Generamos el arbol xml que va a colgar de childevents
            event_child_2 = ET.SubElement(child_event, "event")
            event_child_2.set("type", "CG1")

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
            # for clave, diccionario_sobre_diccionario in diccionario_interno.items():
            #    if clave.startswith('Tipo3_'):
            #        print(diccionario_sobre_diccionario["HORA_DE_COMIENZO"])


    nombre_fichero_sin_extension = os.path.splitext(os.path.basename(archivo))[0]

    with open(directorio_salida + "/" + nombre_fichero_sin_extension + ".mpl", "w", encoding="utf-8") as xml_file:
        # Obtener una representación en cadena de texto del XML y formatear el XML
        xml_str = ET.tostring(marinaPlaylist, encoding="utf-8")
        xml_formatted = xml.dom.minidom.parseString(xml_str).toprettyxml()

        # Escribir el XML formateado en el archivo
        xml_file.write(xml_formatted)
        print("XML generado exitosamente.")
