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


def main():
    carpeta_entrada = seleccionar_carpeta("Selecciona la carpeta de entrada")
    if not carpeta_entrada:
        return

    carpeta_salida = seleccionar_carpeta("Selecciona la carpeta de salida")
    if not carpeta_salida:
        return

    modificados = procesar_archivos(carpeta_entrada, carpeta_salida)
    print(f"Se modificaron {modificados} archivos .marl.")  # Mensaje en consola solamente

def esperar_hasta_manana_a_las_9():
    ahora = datetime.now()
    manana = ahora + timedelta(days=1)
    objetivo = datetime.combine(manana.date(), datetime.min.time()).replace(hour=9)
    segundos_espera = (objetivo - ahora).total_seconds()
    print(f"Esperando hasta las 09:00 del {manana.strftime('%Y-%m-%d')}...")

    # Cuenta atrás
    for restante in range(int(segundos_espera), 0, -1):
        mins, secs = divmod(restante, 60)
        tiempo_str = f"{mins:02d}:{secs:02d}"
        print(f"\rTiempo restante: {tiempo_str}", end="", flush=True)
        time.sleep(1)
    print("\n")

if __name__ == "__main__":
    while True:
        main()
        esperar_hasta_manana_a_las_9()
