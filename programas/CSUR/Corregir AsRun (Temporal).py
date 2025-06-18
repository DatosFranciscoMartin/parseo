import os
import re
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog
from datetime import datetime, timedelta
import time

def seleccionar_carpeta(titulo):
    root = Tk()
    root.withdraw()
    carpeta = filedialog.askdirectory(title=titulo)
    root.destroy()
    return carpeta

def eliminar_eventos_blq(root):
    """
    Elimina todos los elementos <event> cuyo atributo 'type' sea 'Blq Agrupado IN' o 'Blq Agrupado OUT'
    """
    for parent in root.findall('.//'):
        for event in list(parent):
            if event.tag == 'event' and 'type' in event.attrib:
                tipo = event.attrib['type']
                if tipo in ('Blq Agrupado IN', 'Blq Agrupado OUT'):
                    parent.remove(event)

def limpiar_eventos_xml(root):
    """
    Elimina todos los elementos <event> cuyo atributo 'type' contenga 'CG'
    """
    for child_events in root.findall('.//childEvents'):
        for child in list(child_events):
            child_events.remove(child)

def eliminar_eventos_manual_secondary(root):
    """
    Elimina todos los elementos <event> que tengan manualSecondary="true".
    """
    for parent in root.findall('.//'):
        for event in list(parent):
            if (
                event.tag == 'event' and
                event.attrib.get('manualSecondary', '').lower() == 'true'
            ):
                parent.remove(event)

def borra_carpeta_destino(carpeta):

    # Tiempo actual en segundos
    ahora = time.time()

    # Número de segundos en 7 días
    siete_dias = 7 * 24 * 60 * 60

    # Recorrer la carpeta y subcarpetas
    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_archivo = os.path.join(carpeta_actual, archivo)
            # Obtener la última fecha de modificación del archivo
            tiempo_modificacion = os.path.getmtime(ruta_archivo)
            # Si es más antiguo que 7 días, eliminarlo
            if ahora - tiempo_modificacion > siete_dias:
                os.remove(ruta_archivo)

def procesar_archivos(carpeta_entrada, carpeta_salida):
    archivos_modificados = 0
    hoy = datetime.now()

    patron_fecha = re.compile(r'_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})')

    for carpeta_actual, _, archivos in os.walk(carpeta_entrada):
        for archivo in archivos:
            if archivo.lower().endswith('.marl'):
                match = patron_fecha.search(archivo)
                if not match:
                    print(f"Fecha no encontrada en el archivo: {archivo}")
                    continue

                fecha_str = match.group(1)
                try:
                    fecha_archivo = datetime.strptime(fecha_str, "%Y-%m-%d_%H-%M-%S")
                except ValueError:
                    print(f"Formato de fecha inválido en: {archivo}")
                    continue

                if fecha_archivo.date() >= hoy.date():
                    print(f"Saltado (futura o actual): {archivo}")
                    continue

                ruta_completa = os.path.join(carpeta_actual, archivo)
                ruta_relativa = os.path.relpath(ruta_completa, carpeta_entrada)
                ruta_destino = os.path.join(carpeta_salida, ruta_relativa)

                if os.path.exists(ruta_destino):
                    print(f"Saltado (ya existe): {ruta_destino}")
                    continue

                os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)

                try:
                    # Leer archivo como XML estructurado
                    tree = ET.parse(ruta_completa)
                    root = tree.getroot()

                    # Aplicar funciones de limpieza (si devuelven root o modifican in-place)
                    eliminar_eventos_blq(root)
                    limpiar_eventos_xml(root)
                    eliminar_eventos_manual_secondary(root)

                    # Cambiar nombres en <source channelName="...">
                    for source in root.findall('.//source'):
                        canal = source.attrib.get('channelName')
                        if canal == 'ANDALUCIA TV':
                            source.set('channelName', 'ATV [A]')
                        elif canal == 'Canal Sur Andalucia':
                            source.set('channelName', 'CS3 [A]')
                        elif canal == 'Canal Sur 1':
                            source.set('channelName', 'CS1 [A]')

                    # Cambiar txList en <asRun>
                    for asrun in root.findall('.//asRun'):
                        txlist = asrun.attrib.get('txList')
                        if asrun == 'CS 1 [A]':
                            source.set('txList', 'CS1 [A]')
                        elif asrun == 'Canal Sur Andalucia':
                            source.set('txList', 'CS3 [A]')

                    # Guardar XML modificado
                    tree.write(ruta_destino, encoding='utf-8', xml_declaration=True)

                except Exception as e:
                    print(f"Error al procesar {ruta_completa}: {e}")

    return archivos_modificados

def iniciar_monitoreo_periodico(carpeta_entrada, carpeta_salida):
    print("Iniciando escaneo periódico del directorio:", carpeta_entrada)
    try:
        while True:
            modificados = procesar_archivos(carpeta_entrada, carpeta_salida)

            borrar_carpeta_destino(carpeta_salida)

            print(f"Se modificaron {modificados} archivos .marl.")  # Mensaje en consola solamente

            total_segundos = 3600  # 60 minutos
            print("Esperando 1 hora para la siguiente ejecución...")
            for restante in range(total_segundos, 0, -1):
                mins, secs = divmod(restante, 60)
                tiempo_str = f"{mins:02d}:{secs:02d}"
                print(f"\rTiempo restante: {tiempo_str}", end="", flush=True)
                time.sleep(1)
            print("\n")
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")


carpeta_entrada = seleccionar_carpeta("Selecciona la carpeta de entrada")

carpeta_salida = seleccionar_carpeta("Selecciona la carpeta de salida")

iniciar_monitoreo_periodico(carpeta_entrada, carpeta_salida)
