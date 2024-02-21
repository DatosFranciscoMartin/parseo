import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
from datetime import timedelta, datetime


# Fichero de prueba
#ruta = open(r"C:\Users\franciscojavier.mart\Documents\parseo\trf programa\S5231004_10031723.TRF")

#Fichero Real
ruta = r"C:\Users\franciscojavier.mart\Documents\parseo\trf programa\S1240220_12221817.TRF"

# Cargamos la ruta del fichero en una variable para tratarla mas tarde
fichero = open(ruta, "r", encoding="utf-8")


# Sacamos el nombre del fichero en el cual tenemos información acerca de la fecha y hora de creación
nombre_archivo = os.path.basename(ruta)

# La fecha de inicio la sacamos de la siguiente forma sobre el nombre del fichero
fecha_inicio = "20" + nombre_archivo[2:4]+"-"+nombre_archivo[4:6]+"-"+nombre_archivo[6:8]

# Transformamos la fecha de inicio a un objeto de tipo datetime
fecha_transformada = datetime.strptime(fecha_inicio, "%Y-%m-%d")

# Sumamos un dia a la fecha ya transformada
fecha_fin = fecha_transformada + timedelta(days=1)

# Transformamos la fecha de fin a una cadena de texto para usarla mas adelante
fecha_fin_transformada = fecha_fin.strftime("%Y-%m-%d")

# Nos saltamos la primera linea del fichero ya que este no es necesaria
primera_linea = fichero.readline()

# Creamos un diccionario vacío en el que vamos a ir guardando diccionarios que van a corresponder a cada uno de los eventos que tenemos en los ficheros TRF, se guardarian solo los tiopos 1, 4 y 5 ya que los elementos
# de tipo 2 y 3 siempre van dentro de los elementos de tipo 1
eventos = {}

# Generamos 3 contados que nos van a ayudar a generar el numero de eventos que vamos a tener, con los contadores de tipo nos ayuda a poder generar diccionarios dentro de los eventos de tipo 1
contador = 0
contador_tipo_2 = 0
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
        TIHOINMIN = linea[19:30] # HORA DE INICIO
        TIDUMINUT = linea[30:41]
        TITITELEME = linea[41:107]
        LENGUAJE_DE_SIGNOS = linea[107:108]
        AUDIODESCRIPCION = linea[108:109]
        RELACION_DE_ASPECTO = linea[110:111]
        TIPO_DE_AUDIO  = linea[111:114]
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


        #print(CLASIFICACION+RELACION_DE_ASPECTO+TXTAUD+TITIPELEME+CONTRATO+PASE+TICODELEMENMIN+TICODELEMENMIN[11:]+"_"+TIHOINMIN[:8])
        RECONCILEKEY = CLASIFICACION+RELACION_DE_ASPECTO+TXTAUD+TITIPELEME+CONTRATO+PASE+TICODELEMENMIN[:11]+TICODELEMENMIN[11:13]+"_"+TIHOINMIN[:8]
        #print(RECONCILEKEY.replace(" ", "*"))

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
        contador_tipo_2 += 1

        # Aqui guardamos todos los campos que nos interesan dentro de un diccionario que vamos a guardar en el evento de tipo 1 con el numero de evento
        eventos[contador]["Tipo2"+"_"+str(contador_tipo_2)] = {
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
        eventos[contador]["Tipo3"+"_"+str(contador_tipo_3)] = {
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


#for event, diccionario_interno in eventos.items():
#    print(diccionario_interno)


# Crear el elemento raíz del XML, este debe de se de la siguiente forma, siempre va a ser asi:  
marinaPlaylist = ET.Element("marinaPlaylist")
marinaPlaylist.set ("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
marinaPlaylist.set ("xsi:noNamespaceSchemaLocation","./../../../playlist/playlist.xsd")
marinaPlaylist.set ("version","3.1")
marinaPlaylist.set ("comment","PebbleBeach Marina playlist generated by DatosMedia")
marinaPlaylist.set ("StartTime", str(fecha_inicio)+"T01:00:00:00")
marinaPlaylist.set ("EndTime", str(fecha_fin_transformada)+"T00:59:59:24")
properties = ET.SubElement(marinaPlaylist, "properties")
eventlist = ET.SubElement(marinaPlaylist, "eventList")


# En la siguiente iteración vamos a recorrer los eventos que hemos guardado en el diccionario de eventos, y vamos a crear dos variables, event para saber el numero de evento y 
#diccionario_interno para saber el diccionario que vamos a usar para crear el evento

for event, diccionario_interno in eventos.items():

# Si es tipo 4, vamos a seguir la siguiente logica para generar una rama XML de tipo 4

    if diccionario_interno['TIPOREG'] == "4":
        event4 = ET.SubElement(eventlist, "event")
        event4.set("type", "BlockStart")
        properties5 = ET.SubElement(event4, "properties")
        properties5.set("blockname", diccionario_interno["IDBLOQUE"].rstrip())


# Si es tipo 5, vamos a seguir la siguiente logica para generar una rama XML de tipo 5

    if diccionario_interno['TIPOREG'] == "5":
        event5 = ET.SubElement(eventlist, "event")
        event5.set("type", "Comment")  # Aquí puede variar el tipo
        properties5 = ET.SubElement(event5, "properties")
        schedule5 = ET.SubElement(properties5, "schedule")
        schedule5.set("startType", "Sequential")
        event5_1 = ET.SubElement(properties5, "event")
        comment5 = ET.SubElement(event5_1, "comment")
        comment5.text = diccionario_interno["OBSERVACIONES"].rstrip()
    
# Si tipo1
# Si en este caso es tipo directo, o lo que es lo mismo, el valor del campo DIRGRAB es D seguimos la siguiente logica
        
    if diccionario_interno['TIPOREG'] == "1" and diccionario_interno['DIRGRAB'] == "D":
        event1 = ET.SubElement(eventlist, "event")
        event1.set("type", "Live")
        properties1 = ET.SubElement(event1, "properties")
        schedule1 = ET.SubElement(properties1, "schedule")
        schedule1.set("endType", "Hold")
        schedule1.set("endOffset", diccionario_interno['TIDUMINUT'])
        media1 = ET.SubElement(properties1, "media")
        media1.set("mediaType", "Live")
        media1.set("mediaName", diccionario_interno["TICODELEMENMIN"].rstrip()),
        #media1.set("mediaName", "TESTOK"),

        # Se agrega etiquetas comunes de ambos casos
        event1_2 = ET.SubElement(properties1, "event")
        event1_2.set("title", diccionario_interno["TITITELEME"].rstrip())
        event1_2.set("reconcileKey", diccionario_interno["RECONCILEKEY"])
        classifications1 = ET.SubElement(event1_2, "classifications")
        classification1 = ET.SubElement(classifications1, "classification")
        classification1.set("classification", "EventType")
        classification1.set("category", diccionario_interno["TITIPELEME"])
        mediaStream1 = ET.SubElement(properties1, "mediaStream")
        mediaStream1.set("som", diccionario_interno["TIHOINMIN"])

        # Se comprueba si es tipo fijo o tipo secuencial
        if diccionario_interno['INDELEMFIJO'] == "F":
                schedule1.set("startType", "Fixed")
                schedule1.set("startOffset", fecha_inicio+"T"+diccionario_interno['TIHOINMIN'])
        else:
            schedule1.set("startType", "Sequential")
        
        # Recorremos los diccionarios de tipo 3 y tipo 2 si los hubiera.
        for clave, diccionario_sobre_diccionario in diccionario_interno.items():
            if clave.startswith('Tipo3_'):
                print(diccionario_sobre_diccionario["HORA_DE_COMIENZO"])




# Si en este caso es tipo grabado, o lo que es lo mismo, el valor del campo DIRGRAB es G
    if diccionario_interno['TIPOREG'] == "1" and diccionario_interno['DIRGRAB'] == "G":
        event1 = ET.SubElement(eventlist, "event")
        event1.set("type", "PrimaryVideo")
        properties1 = ET.SubElement(event1, "properties")
        schedule1 = ET.SubElement(properties1, "schedule")
        schedule1.set("endType", "Duration")
        schedule1.set("endOffset", diccionario_interno['TIDUMINUT'])
        media1 = ET.SubElement(properties1, "media")
        media1.set("mediaType", "Video")
        media1.set("mediaName", diccionario_interno["TICODELEMENMIN"].rstrip())
        #media1.set("mediaName", "TESTOK"),
        mediaStream1 = ET.SubElement(properties1, "mediaStream")
        mediaStream1.set("som", diccionario_interno['TIHOINMIN'].rstrip())
        video1 = ET.SubElement(mediaStream1,"video")
        video1.set("jobType", "Play")
        segment1 = ET.SubElement(mediaStream1,"segment")
        segment1.set("type", "Media")

        # Se agrega etiquetas comunes de ambos casos
        event1_2 = ET.SubElement(properties1, "event")
        event1_2.set("title", diccionario_interno["TITITELEME"].rstrip())
        event1_2.set("reconcileKey", diccionario_interno["RECONCILEKEY"])
        classifications1 = ET.SubElement(event1_2, "classifications")
        classification1 = ET.SubElement(classifications1, "classification")
        classification1.set("classification", "EventType")
        classification1.set("category", diccionario_interno["TITIPELEME"])
        mediaStream1 = ET.SubElement(properties1, "mediaStream")
        mediaStream1.set("som", diccionario_interno["TIHOINMIN"].rstrip())

        # Se comprueba si es tipo fijo o tipo secuencial
        if diccionario_interno['INDELEMFIJO'] == "F":
            schedule1.set("startType", "Fixed")
            schedule1.set("startOffset", fecha_inicio+"T"+diccionario_interno['TIHOINMIN'])
        else:
            schedule1.set("startType", "Sequential")
        
        # Recorremos los diccionarios de tipo 3 y tipo 2 si los hubiera.
        for clave, diccionario_sobre_diccionario in diccionario_interno.items():
            if clave.startswith('Tipo3_'):
                print(diccionario_sobre_diccionario["HORA_DE_COMIENZO"])




# Crear el objeto ElementTree para representar la estructura del XML
tree = ET.ElementTree(marinaPlaylist)

# Escribir el árbol XML en un archivo
with open(r"C:\Users\franciscojavier.mart\Documents\parseo\prueba_final.mpl", "w", encoding="utf-8") as xml_file:
    # Obtener una representación en cadena de texto del XML y formatear el XML
    xml_str = ET.tostring(marinaPlaylist, encoding="utf-8")
    xml_formatted = xml.dom.minidom.parseString(xml_str).toprettyxml()

    # Escribir el XML formateado en el archivo
    xml_file.write(xml_formatted)
    print("XML generado exitosamente.")