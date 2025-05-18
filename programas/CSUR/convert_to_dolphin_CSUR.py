import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
    Este fragmento de código Python define una función procesar_archivo que procesa un archivo MPL. Extrae información del archivo de entrada, manipula los datos y escribe la salida formateada en un nuevo archivo. 
    El código incluye operaciones como la lectura de líneas específicas, la extracción de subcadenas y la escritura de datos formateados en un archivo de salida. 
    También registra el nombre del fichero procesado e imprime un mensaje en la consola.
    """
    # Generamos el nombre del fichero para el log, eliminamos la ruta absoluta y nos quedamos solo con el nombre del fichero
    nombre_archivo = os.path.basename(archivo)
    logging.info(f"Archivo procesado: {nombre_archivo}")

    # Determinar carpeta de salida según el comienzo del nombre
    if nombre_archivo.startswith("CS1_ALMERIA"):
        subcarpeta = os.path.join("Provinciales", "ALMERIA")
    elif nombre_archivo.startswith("CS1_CADIZ"):
        subcarpeta = os.path.join("Provinciales", "CADIZ")
    elif nombre_archivo.startswith("CS1_CORDOBA"):
        subcarpeta = os.path.join("Provinciales", "CORDOBA")
    elif nombre_archivo.startswith("CS1_GRANADA"):
        subcarpeta = os.path.join("Provinciales", "GRANADA")
    elif nombre_archivo.startswith("CS1_JAEN"):
        subcarpeta = os.path.join("Provinciales", "JAEN")
    elif nombre_archivo.startswith("CS1_HUELVA"):
        subcarpeta = os.path.join("Provinciales", "HUELVA")
    elif nombre_archivo.startswith("CS1_MALAGA"):
        subcarpeta = os.path.join("Provinciales", "MALAGA")
    elif nombre_archivo.startswith("CS1"):
        subcarpeta = "CS1"
    elif nombre_archivo.startswith("CS2"):
        subcarpeta = "CS2"
    elif nombre_archivo.startswith("CS3"):
        subcarpeta = "CS3"
    elif nombre_archivo.startswith("CS3_IP"):
        subcarpeta = "YOUTUBE"
    elif nombre_archivo.startswith("CS4"):
        subcarpeta = "ATV"
    elif nombre_archivo.startswith("CS5"):
        subcarpeta = "CS5"
    else:
        print("Archivo no procesado. Nombre de archivo no compatible:", archivo)
        return  # No se procesa el archivo si no coincide

    #Mensaje en la consola de salida que se indica que fichero se esta procesando.

    print("Procesando archivo:", archivo)

    tree = ET.parse(archivo)
    root = tree.getroot()

    ###### ESTO AÑADE EL SUBTITULO EN DIRECTO

    # Encontrar el evento de tipo 'Live'

    for event in root.findall(".//event[@type='Live']"):
        # Crear el nuevo feature de subtítulos
        feature_subtitle = ET.Element("feature", type="Subtitle")
        properties = ET.SubElement(feature_subtitle, "properties")

        media_stream = ET.SubElement(properties, "mediaStream")
        subtitle = ET.SubElement(media_stream, "subtitle", source="Live")

        allocation = ET.SubElement(media_stream, "allocation", type="ListStream")
        list_stream = ET.SubElement(allocation, "listStream", type="Fixed", listStreamNo="0")

        media = ET.SubElement(properties, "media", mediaType="Subtitle", mediaName="LIVE")

        # Agregar el nuevo feature dentro de las características del evento Live
        features = event.find(".//features")
        if features is None:
            features = ET.SubElement(event, "features")

        features.append(feature_subtitle)


    ###### ESTO CAMBIA EL COMBINADOR DE AUDIOc

    # Seleccionar todos los elementos <feature> con type="Combinador Audio"
    elementosFeature = root.findall('.//feature[@type="Combinador Audio"]')

    if len(elementosFeature) > 0:
        # Nuevo valor para el atributo "type"
        nuevoTipo = "AudioShuffle"

        # Iterar a través de los elementos y cambiar el valor del atributo "type"
        for elementoFeature in elementosFeature:
            elementoFeature.set("type", nuevoTipo)

    ###### ESTO CAMBIA EL LOGOHD

    # Encontrar todos los elementos <event> que cumplan con la condición
    elementosEvent = root.findall('.//event[@type="Logo"]')

    try:
        if len(elementosEvent) > 0:
            for elementoEvent in elementosEvent:
                # Buscar y eliminar el bloque de <features> con <feature type="LogoHD">
                elementoFeatures = elementoEvent.find('./properties/features')
                elementoFeatureLogoHD = elementoFeatures.find('./feature[@type="LogoHD"]')

                if elementoFeatureLogoHD is not None:
                    elementoFeatures.remove(elementoFeatureLogoHD)
    except:
        print("No se encontraron elementos <event> con el atributo 'type' igual a 'LogoHD'")

    ###### ESTO CAMBIA EL LOGO

    # Seleccionar todos los elementos <event> con type="Logo"
    elementosFeature = root.findall('.//event[@type="Logo"]')

    if len(elementosFeature) > 0:
        # Nuevo valor para el atributo "type"
        nuevoTipo = "CG 4"

        # Iterar a través de los elementos y cambiar el valor del atributo "type"
        for elementoFeature in elementosFeature:
            elementoFeature.set("type", nuevoTipo)

    ###### ESTO CAMBIA EL CG

    # Seleccionar todos los elementos <event> con type="CG"
    elementosFeature = root.findall('.//event[@type="CG"]')

    if len(elementosFeature) > 0:
        # Nuevo valor para el atributo "type"
        nuevoTipo = "CG 3"

        # Iterar a través de los elementos y cambiar el valor del atributo "type"
        for elementoFeature in elementosFeature:
            elementoFeature.set("type", nuevoTipo)

    ###### ESTO CAMBIA EL Orad

    # Seleccionar todos los elementos <event> con type="Orad"

    for event in root.findall(".//event[@type='Orad']"):
        media_stream = event.find(".//mediaStream")

        if media_stream is not None and media_stream.find(".//cg[@type='Template']") is not None:
            # Encontrar todos los elementos <f> dentro del nodo <cg> de tipo Template
            cg = media_stream.find(".//cg[@type='Template']")
            fields = cg.findall("f")

            # Reiniciar el índice a 1 para cada evento CG de tipo Template
            for idx, field in enumerate(fields, start=1):
                field.set('name', f'f{idx}')

    elementosFeature = root.findall('.//event[@type="Orad"]')

    if len(elementosFeature) > 0:

        # Iterar a través de los elementos y cambiar el valor del atributo "type"
        for elementoFeature in elementosFeature:
            # Nuevo valor para el atributo "type"

            CG_media = elementoFeature.find(".//media")
            nuevoTipo = "CG"

            if CG_media is not None:
                CG_mediaName = CG_media.get("mediaName")

                if CG_mediaName == "MoscaCS1":
                    nuevoTipo = "CG 2"

                elif CG_mediaName == "MoscaCS1_Acont":
                    nuevoTipo = "CG 2"

                elif CG_mediaName == "MoscaATV":
                    nuevoTipo = "CG 2"

                elif CG_mediaName == "Crawl":
                    nuevoTipo = "CG 3"

            elementoFeature.set("type", nuevoTipo)

    ###### ESTO CAMBIA EL LAYER

    # Seleccionar todos los elementos layer"
    elementosLayer = root.findall('.//event/properties/mediaStream/cg[@layer]')

    if len(elementosLayer) > 0:
        # Nuevo valor para el atributo "layer"
        nuevoLayer = "0"

        # Iterar a través de los elementos y cambiar el valor del atributo "layer"
        for elementoLayer in elementosLayer:
            elementoLayer.set("layer", nuevoLayer)

    # Crear la ruta completa
    ruta_salida = os.path.join(directorio_salida, subcarpeta)

    # Guardar los cambios en el archivo XML
    tree.write(ruta_salida + '/' + nombre_archivo, encoding='utf-8', xml_declaration=True)

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Este código define un método on_created que se llama cuando se crea un fichero. Si el elemento creado es un directorio, no devuelve nada y no se llama a ninguna funcion adicional. 
        Si el elemento creado es un archivo .MPL, llama a una función procesar_archivo con la ruta del archivo creado como argumento.
        """
        if event.is_directory:
            return
        if event.src_path.endswith('.mpl'):
            time.sleep(1)
            archivo = event.src_path
            procesar_archivo(archivo)


# La siguiente funcion inicia el monitoreo en el directorio que, nosotros le indiquemos en el GUI que nos salta cuando iniciamos el programa
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