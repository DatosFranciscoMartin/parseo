import os
import re
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog, messagebox
from datetime import datetime
import time
from datetime import datetime, timedelta

def seleccionar_carpeta(titulo):
    root = Tk()
    root.withdraw()
    carpeta = filedialog.askdirectory(title=titulo)
    root.destroy()
    return carpeta

def eliminar_eventos_blq(contenido):
    patron_evento = re.compile(
        r'\s*<event[^>]+type="Blq Agrupado (IN|OUT)"[^>]*>.*?</event>\s*',
        re.DOTALL
    )
    return re.sub(patron_evento, '', contenido)

def revertir_cambios_xml(xml_str):
    try:
        root = ET.fromstring(xml_str)

        for feature in root.findall('.//feature[@type="AudioShuffle"]'):
            feature.set("type", "Combinador Audio")

        for event in root.findall('.//event[@type="CG 4"]'):
            event.set("type", "Logo")

        for event in root.findall('.//event[@type="CG 3"]'):
            event.set("type", "CG")

        for event in root.findall('.//event[@type="CG 2"]') + root.findall('.//event[@type="CG 3"]'):
            media = event.find(".//media")
            if media is not None:
                mediaName = media.get("mediaName")
                if mediaName in ["MoscaCS1", "MoscaCS1_Acont", "MoscaATV", "Crawl"]:
                    event.set("type", "Orad")

        for event in root.findall(".//event[@type='Live']"):
            features = event.find(".//features")
            if features is not None:
                for feature in features.findall("feature[@type='Subtitle']"):
                    features.remove(feature)

        return ET.tostring(root, encoding='unicode')

    except ET.ParseError:
        return xml_str

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
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        contenido = f.read()

                    nuevo_contenido = contenido.replace('CS 1 [', 'CS1 [')
                    nuevo_contenido = nuevo_contenido.replace('CS Andalucia [', 'CS3 [')
                    nuevo_contenido = nuevo_contenido.replace(
                        "<source channelName='Canal Sur 1'/>",
                        "<source channelName='CS1 [A]'/>"
                    )
                    nuevo_contenido = nuevo_contenido.replace(
                        "<source channelName='ANDALUCIA TV'/>",
                        "<source channelName='ATV [A]'/>"
                    )
                    nuevo_contenido = nuevo_contenido.replace(
                        "<source channelName='Canal Sur Andalucia'/>",
                        "<source channelName='CS3 [A]'/>"
                    )

                    nuevo_contenido = eliminar_eventos_blq(nuevo_contenido)
                    nuevo_contenido = revertir_cambios_xml(nuevo_contenido)

                    with open(ruta_destino, 'w', encoding='utf-8') as f:
                        f.write(nuevo_contenido)

                    archivos_modificados += 1

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
    messagebox.showinfo("Proceso terminado", f"Se modificaron {modificados} archivos .marl.")

def esperar_hasta_manana_a_las_9():
    ahora = datetime.now()
    manana = ahora + timedelta(days=1)
    objetivo = datetime.combine(manana.date(), datetime.min.time()).replace(hour=9)
    segundos_espera = (objetivo - ahora).total_seconds()
    print(f"Esperando hasta mañana a las 09:00... ({int(segundos_espera)} segundos)")
    time.sleep(segundos_espera)

if __name__ == "__main__":
    while True:
        main()
        esperar_hasta_manana_a_las_9()

