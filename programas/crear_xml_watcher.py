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
    # La fecha de inicio la sacamos de la siguiente forma sobre el nombre del fichero
    fecha_inicio = "20" + nombre_archivo[2:4]+"-"+nombre_archivo[4:6]+"-"+nombre_archivo[6:8]

    # Transformamos la fecha de inicio a un objeto de tipo datetime
    fecha_transformada = datetime.strptime(fecha_inicio, "%Y-%m-%d")

    # Sumamos un dia a la fecha ya transformada
    fecha_fin = fecha_transformada + timedelta(days=1)

    # Transformamos la fecha de fin a una cadena de texto para usarla mas adelante
    fecha_fin_transformada = fecha_fin.strftime("%Y-%m-%d")

    #Mensaje en la consola de salida que se indica que fichero se esta procesando.

    print("Procesando archivo:", archivo)

    with open(archivo, "r", encoding="utf-8") as fichero:
        primera_linea = fichero.readline()
        eventos = {}

    # Generamos 3 contadores que nos van a ayudar a generar el numero de eventos que vamos a tener, con los contadores de tipo nos ayuda a poder generar diccionarios dentro de los eventos de tipo 1
        contador = 0
        contador_tipo_2 = 0
        contador_tipo_3 = 0
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
            #for clave, diccionario_sobre_diccionario in diccionario_interno.items():
            #    if clave.startswith('Tipo3_'):
            #        print(diccionario_sobre_diccionario["HORA_DE_COMIENZO"])
            #    elif clave.startswith('Tipo2_'):
            #        print(diccionario_sobre_diccionario["HORA_ANUNCIADA"])





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
            #for clave, diccionario_sobre_diccionario in diccionario_interno.items():
            #    if clave.startswith('Tipo3_'):
            #        print(diccionario_sobre_diccionario["HORA_DE_COMIENZO"])
            #    elif clave.startswith('Tipo2_'):
            #        print(diccionario_sobre_diccionario["HORA_ANUNCIADA"])




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
