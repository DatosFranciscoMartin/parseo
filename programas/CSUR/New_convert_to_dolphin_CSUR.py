import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import os
import time
import logging

# --- GUI para seleccionar carpetas ---

def seleccionar_directorio_a_monitorizar():
    global directorio_monitorizar
    directorio_monitorizar = filedialog.askdirectory()
    if directorio_monitorizar:
        etiqueta_directorio_monitorizar.config(text="Directorio a monitorizar seleccionado:\n" + directorio_monitorizar)

def seleccionar_directorio_salida():
    global directorio_salida
    directorio_salida = filedialog.askdirectory()
    if directorio_salida:
        etiqueta_directorio_salida.config(text="Directorio de salida seleccionado:\n" + directorio_salida)

def salir():
    ventana.destroy()

ventana = tk.Tk()
ventana.geometry("600x400")
ventana.title("Seleccionar directorio a monitorizar y directorio de salida")

tk.Button(ventana, text="Seleccionar directorio a monitorizar", command=seleccionar_directorio_a_monitorizar).pack(pady=10)
etiqueta_directorio_monitorizar = tk.Label(ventana, text="Ningún directorio de salida seleccionado")
etiqueta_directorio_monitorizar.pack()

tk.Button(ventana, text="Seleccionar directorio de salida", command=seleccionar_directorio_salida).pack(pady=10)
etiqueta_directorio_salida = tk.Label(ventana, text="Ningún directorio de salida seleccionado")
etiqueta_directorio_salida.pack()

tk.Button(ventana, text="Ejecutar", command=salir).pack(pady=10)

ventana.mainloop()

# --- Configuración de logs ---
log_file = os.path.join(directorio_salida, "log.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M')

# --- Historial de archivos procesados persistente ---
historial_path = os.path.join(directorio_salida, "procesados.txt")

def cargar_historial():
    if os.path.exists(historial_path):
        with open(historial_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    return set()

def guardar_en_historial(ruta_archivo):
    with open(historial_path, "a", encoding="utf-8") as f:
        f.write(ruta_archivo + "\n")

# --- Procesamiento de archivos ---

def procesar_archivo(archivo):
    nombre_archivo = os.path.basename(archivo)
    logging.info(f"Archivo procesado: {nombre_archivo}")

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
    elif nombre_archivo.startswith("CS3_IP"):
        subcarpeta = "YOUTUBE"
    elif nombre_archivo.startswith("CS3"):
        subcarpeta = "CSA"
    elif nombre_archivo.startswith("CS4"):
        subcarpeta = "ATV"
    elif nombre_archivo.startswith("CS5"):
        subcarpeta = "CS5"
    else:
        print("Archivo no procesado. Nombre de archivo no compatible:", archivo)
        return

    print("Procesando archivo:", archivo)

    tree = ET.parse(archivo)
    root = tree.getroot()

    for event in root.findall(".//event[@type='Live']"):
        feature_subtitle = ET.Element("feature", type="Subtitle")
        properties = ET.SubElement(feature_subtitle, "properties")
        media_stream = ET.SubElement(properties, "mediaStream")
        subtitle = ET.SubElement(media_stream, "subtitle", source="Live")
        allocation = ET.SubElement(media_stream, "allocation", type="ListStream")
        list_stream = ET.SubElement(allocation, "listStream", type="Fixed", listStreamNo="0")
        media = ET.SubElement(properties, "media", mediaType="Subtitle", mediaName="LIVE")
        features = event.find(".//features")
        if features is None:
            features = ET.SubElement(event, "features")
        features.append(feature_subtitle)

    for elementoFeature in root.findall('.//feature[@type="Combinador Audio"]'):
        elementoFeature.set("type", "AudioShuffle")
        elementoFeatureproperties = elementoFeature.find('properties')
        if elementoFeatureproperties is not None:
            # Buscamos el único macro
            macro = elementoFeatureproperties.find('macro')
            valor_macro = macro.get('value') if macro is not None else "STEREO"

            # Creamos la nueva estructura
            effect = ET.Element('effect', {'status': 'On', 'type': 'Audio Shuffle'})
            audioShuffle = ET.SubElement(effect, 'audioShuffle', {'type': 'TrackPreset'})
            ET.SubElement(audioShuffle, 'trackPreset', {'name': valor_macro})

            # Limpiamos todo dentro de properties (borramos macro también)
            for child in list(elementoFeatureproperties):
                elementoFeatureproperties.remove(child)

            # Añadimos effect dentro de properties
            elementoFeatureproperties.append(effect)

    for elementoEvent in root.findall('.//event[@type="Logo"]'):
        try:
            features = elementoEvent.find('./properties/features')
            logo_hd = features.find('./feature[@type="LogoHD"]')
            if logo_hd is not None:
                features.remove(logo_hd)
        except:
            print("No se encontraron elementos <event> con el atributo 'type' igual a 'LogoHD'")

    for elementoFeature in root.findall('.//event[@type="Logo"]'):
        elementoFeature.set("type", "CG 4")

    for elementoFeature in root.findall('.//event[@type="CG"]'):
        elementoFeature.set("type", "CG 3")

    for event in root.findall(".//event[@type='Orad']"):
        media_stream = event.find(".//mediaStream")
        if media_stream is not None and media_stream.find(".//cg[@type='Template']") is not None:
            cg = media_stream.find(".//cg[@type='Template']")
            for idx, field in enumerate(cg.findall("f"), start=1):
                field.set('name', f'f{idx}')

    for elementoFeature in root.findall('.//event[@type="Orad"]'):
        media = elementoFeature.find(".//media")
        nuevoTipo = "CG"
        if media is not None:
            mediaName = media.get("mediaName")
            if mediaName in ["MoscaCS1", "MoscaCS1_Acont", "MoscaATV"]:
                nuevoTipo = "CG 2"
            elif mediaName == "Crawl":
                nuevoTipo = "CG 3"
        elementoFeature.set("type", nuevoTipo)

    for layer in root.findall('.//event/properties/mediaStream/cg[@layer]'):
        layer.set("layer", "0")

    ruta_salida = os.path.join(directorio_salida, subcarpeta)
    os.makedirs(ruta_salida, exist_ok=True)
    tree.write(os.path.join(ruta_salida, nombre_archivo), encoding='utf-8', xml_declaration=True)

# --- Escaneo periódico ---

archivos_procesados = cargar_historial()

def escanear_directorio():
    for carpeta_actual, _, archivos in os.walk(directorio_monitorizar):
        for archivo in archivos:
            if archivo.endswith(".mpl"):
                ruta_archivo = os.path.join(carpeta_actual, archivo)
                if ruta_archivo not in archivos_procesados:
                    try:
                        procesar_archivo(ruta_archivo)
                        archivos_procesados.add(ruta_archivo)
                        guardar_en_historial(ruta_archivo)
                    except Exception as e:
                        logging.error(f"Error al procesar {ruta_archivo}: {str(e)}")

def iniciar_monitoreo_periodico():
    print("Iniciando escaneo periódico del directorio:", directorio_monitorizar)
    try:
        while True:
            escanear_directorio()
            time.sleep(60)  # Espera de 1 minuto
    except KeyboardInterrupt:
        print("Monitoreo detenido por el usuario.")

# --- Punto de entrada del programa ---

if __name__ == "__main__":
    iniciar_monitoreo_periodico()
