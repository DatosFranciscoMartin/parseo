import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom


# Cargar el archivo de configuración
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'cf', 'config.conf'))

# Obtener las rutas desde la configuración
rutas = config['rutas']
ruta_watch = rutas['ruta_watcher']
ruta_salida = rutas['ruta_salida']


def procesar_archivo(archivo):
    with open(archivo, "r", encoding="utf-8-sig") as fichero:
        _, extension = os.path.splitext(archivo)
        mediaType = "Video"
        hora_actual = datetime.now()
        creationTime = hora_actual.strftime("%H:%M:%S:%f")[:11]
        mediaRecords = ET.Element("mediaRecords")

        if extension == ".dub":
            # Leer todas las líneas del archivo
            lineas = fichero.readlines()

            for linea in lineas[2:]:

                # Eliminar espacios en blanco al inicio y final de la línea
                linea = linea.strip()

                # Dividir la línea en variables
                variables = linea.split()

                Som = variables[3]
                title = variables[1]
                mediaID = variables[0]

                # Crear el elemento raíz


                # Crear el elemento media y establecer los atributos
                media = ET.SubElement(mediaRecords, "media")
                media.set("mediaName", mediaID)
                media.set("mediaType", mediaType)
                media.set("title", title)
                media.set("origSOM", Som)
                media.set("creationTime", creationTime)

        else:

            # Parsear el archivo XML
            tree = ET.parse(fichero)
            root = tree.getroot()

            # Detectar la estructura del XML
            if root.tag == 'PBSDubList':

                # Inicializar variables
                Som = None
                title = None
                mediaID = None

                # Extraer y mostrar los parámetros de cada DubItem
                for dub_item in root.findall('.//DubItem'):
                    Som = dub_item.find('SOM').text
                    title = dub_item.find('Title').text
                    mediaID = dub_item.find('MediaId').text


                    # Crear el elemento media y establecer los atributos
                    media = ET.SubElement(mediaRecords, "media")
                    media.set("mediaName", mediaID)
                    media.set("mediaType", mediaType)
                    media.set("title", title)
                    media.set("origSOM", Som)
                    media.set("creationTime", creationTime)

            else:

                # Namespace utilizado en el XML
                namespace = {'soa': 'urn:telestream.net:soa:core'}

                # Inicializar variables
                Som = ''
                title = ''
                mediaID = ''

                # Buscar y obtener los valores de IDConti, Title y SOM
                for param in root.findall('.//soa:Parameter', namespace):
                    param_name = param.get('name')
                    param_value = param.text

                    if param_name == "IDConti":
                        mediaID = param_value
                    elif param_name == "Title":
                        title = param_value
                    elif param_name == "SOM":
                        Som  = param_value

                # Extraer y mostrar los parámetros de cada Parameter
                # Namespace utilizado en el XML
                #namespace = {'soa': 'urn:telestream.net:soa:core'}
                #parameters = {}
                #for parameters in root.findall('.//soa:Parameter'):
                #    if parameters.get('name') == 'IDConti':
                #        mediaID = parameters.text
                #    elif parameters.get('name') == 'Title':
                #        title = parameters.text
                #    elif parameters.get('name') == 'SOM':
                #        Som = parameters.text


                # Crear el elemento media y establecer los atributos
                media = ET.SubElement(mediaRecords, "media")
                media.set("mediaName", mediaID)
                media.set("mediaType", mediaType)
                media.set("title", title)
                media.set("origSOM", Som)
                media.set("creationTime", creationTime)

        nombre_fichero_sin_extension = os.path.splitext(os.path.basename(archivo))[0]
        with open(ruta_salida + "/" + nombre_fichero_sin_extension + ".xml", "w", encoding="utf-8") as xml_file:
            # Generar el XML como una cadena
            xml_string = ET.tostring(mediaRecords, encoding="iso-8859-1")

            # Obtener una representación en cadena de texto del XML y formatear el XML
            xml_formatted = xml.dom.minidom.parseString(xml_string).toprettyxml()

            # Escribir el XML formateado en el archivo
            xml_file.write(xml_formatted)
            print("XML generado exitosamente. Se ha creado en " + ruta_salida + "\\" + nombre_fichero_sin_extension + ".xml")

class Watcher:
    """
    Clase que se encarga de monitorear un directorio y ejecutar una función cuando se crea un archivo.
    """

    DIRECTORY_TO_WATCH = ruta_watch  # Ruta del directorio a monitorear

    def __init__(self):
        """
        Inicializa el observador de archivos.
        """
        self.observer = Observer()

    def run(self):
        """
        Ejecuta el observador de archivos para monitorear el directorio especificado.
        """
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    """
    Clase que maneja los eventos de cambios en el sistema de archivos.
    """

    @staticmethod
    def on_any_event(event):
        """
        Método que se ejecuta cuando ocurre un evento en el sistema de archivos.
        """
        if event.is_directory:
            return None  # Ignorar eventos de directorios
        elif event.event_type == 'created':
            # Aquí se maneja el evento de creación de archivos.
            if event.src_path.endswith('.xml') or event.src_path.endswith('.dub'):
                time.sleep(1)
                #print(f"Se ha creado el archivo: {event.src_path}")
                archivo = event.src_path
                procesar_archivo(archivo)

if __name__ == '__main__':
    w = Watcher()
    w.run()