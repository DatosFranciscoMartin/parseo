import tkinter as tk
from tkinter import filedialog
import os
import datetime
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
# ventana.iconbitmap(r"programas\icono_datos.ico")
ventana.title("Seleccionar directorio a monitorizar y directorio de salida")

# Botón para seleccionar directorio a monitorizar
boton_seleccionar_directorio_a_monitorizar = tk.Button(ventana, text="Seleccionar directorio a monitorizar",
                                                       command=seleccionar_directorio_a_monitorizar)
boton_seleccionar_directorio_a_monitorizar.pack(pady=10)

# Etiqueta para mostrar el directorio a monitorizar seleccionado
etiqueta_directorio_monitorizar = tk.Label(ventana, text="Ningún directorio de salida seleccionado")
etiqueta_directorio_monitorizar.pack()

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

# Directorio a monitorear
directorio_a_monitorear = directorio_monitorizar

# Agregado lineas de para generar un log en tiempo real
log_file = os.path.join(directorio_salida, "log.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M')


def procesar_archivo(archivo):
    """
    Este fragmento de código Python define una función procesar_archivo que procesa un archivo marl. Extrae información del archivo de entrada, manipula los datos y escribe la salida formateada en un nuevo archivo.
    El código incluye operaciones como la lectura de líneas específicas, la extracción de subcadenas y la escritura de datos formateados en un archivo de salida.
    También registra el nombre del fichero procesado e imprime un mensaje en la consola.
    """
    # Generamos el nombre del fichero para el log, eliminamos la ruta absoluta y nos quedamos solo con el nombre del fichero
    nombre_archivo = os.path.basename(archivo)
    logging.info(f"Archivo procesado: {nombre_archivo}")

    # Mensaje en la consola de salida que se indica que fichero se esta procesando.

    print("Procesando archivo:", archivo)

    # Abre cada archivo en modo lectura
    with open(archivo, "r", encoding="utf-8") as fichero:

        # Parsear el XML desde el archivo
        tree = ET.parse(fichero)
        root = tree.getroot()

        DEFAULT = "*****************************************************"

        # Lee la siguiente línea que contiene información necesaria

        circuito = root.find('.//source').get('channelName')
        year = root.get('startTime')[2:4]
        mes = root.get('startTime')[5:7]
        dia = root.get('startTime')[8:10]

        contador = 0

        # Abre el archivo de salida en el directorio seleccionado
        # Se crea el fichero en modo escritura bajo el encode utf-8
        with open(os.path.join(directorio_salida, f"{circuito}{year}{mes}{dia}.rgt"), "w",
                  encoding="utf-8") as Archivo_salida:
            Archivo_salida.write(circuito + year + mes + dia + "\n")

            # Otras operaciones para leer el archivo y escribir en el archivo de salida
            for event in root.findall('.//eventList/event'):

                A = event.find('.//asRun').get('endTime').split('T')[1]
                B = event.find('.//properties/event').get('houseId')
                C = DEFAULT[:2]
                D = event.find('.//properties/event').get('title')
                E = event.find('.//asRun').get('duration')
                F = event.find('.//properties/event').get('reconcileKey')[3:4]
                G = event.find('.//properties/event').get('reconcileKey')[1:2]
                if G == " " or G == "0":
                    G = "2"
                H = event.find('.//properties/event').get('reconcileKey')[4:11]
                I = event.find('.//properties/event').get('reconcileKey')[11:14]
                if event.find('.//properties/media').get('mediaName').startswith('B'):
                    J = event.find('.//properties/media').get('mediaName')[1:6]
                else:
                    J = DEFAULT[:5]
                K = event.find('.//properties/event').get('reconcileKey')[14:25]
                L = event.find('.//properties/event').get('reconcileKey')[25:27]
                if event.find('.//properties/event/comment') is not None:
                    M = event.find('.//properties/event/comment').text[0:13]
                else:
                    M = DEFAULT[:14]
                N = DEFAULT[:2]
                O = DEFAULT[:2]
                P = event.find('.//properties/event').get('reconcileKey')[0:1]
                if P == " " or P == "0":
                    P = "7"
                Q = DEFAULT[:1]

                if event.find('.//properties/event').get('reconcileKey')[
                   2:3] == "0":  # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    R = "0"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "1":  # SUBTITULADO == "S" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    R = "1"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "2":  # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    R = "2"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "3":  # SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    R = "7"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "4":  # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    R = "3"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "5":  # SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    R = "D"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "6":  # SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    R = "B"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "7":  # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
                    R = "6"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "8":  # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
                    R = "9"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "9":  # SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
                    R = "A"
                elif event.find('.//properties/event').get('reconcileKey')[
                     2:3] == "A":  # SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
                    R = "C"

                ##"EST": "3-ST",
                ##"DST": "2-DL-ST",
                # "MON": "1-MONO",
                # "DUA": "2-DL-ST-DOLBY",
                # "DP1": "7-DOLBY1",
                # "DP2": "8-DOLBY2",
                ##"DP3": "Dolby PAR 3",
                # "DG1": "5-DUAL5-6",
                ##"DG2": "6-DUAL3-4"

                if event.find('.//properties/features/feature/properties/effect/audioShuffle/trackPreset').get(
                        'name') in ["EST", "DST", "DP3", "DG2"]:
                    S = event.find('.//properties/features/feature/properties/effect/audioShuffle/trackPreset').get(
                        'name')
                else:
                    S = DEFAULT[:3]

                T = DEFAULT[:1]
                if event.find('.//childEvent/event/properties/event/comment').text == "I":
                    U = event.find('.//childEvent/event/properties/media').get('mediaName')
                else:
                    U = DEFAULT[:4]

                V = DEFAULT[:1]
                W = DEFAULT[:1]
                ESPECIAL = DEFAULT[:2]
                X = event.find('.//properties/event').get('reconcileKey')[28:]

                if event.find('.//properties/event').get('reconcileKey')[0:1] in ["1", "2"]:
                    Y = event.find('.//properties/event').get('reconcileKey')[0:1]
                elif event.find('.//properties/event').get('reconcileKey')[0:1] in [" ", "0"]:
                    Y = "0"
                else:
                    Y = DEFAULT[:1]

                # Escribimos en el archivo de salida la línea formateada correctamente.

                Archivo_salida.write(
                    str(A).ljust(11) + "  " + str(B).ljust(18) + "  " + str(C).ljust(2) + "  " + str(D).ljust(32)[
                                                                                                 :32] + "  " + str(
                        E).ljust(11) + "  " + str(F).ljust(1) + " " + str(G).ljust(1) + str(H).ljust(7) + "  " + str(
                        I).ljust(3) + "  " + str(J).ljust(5) + "  " + str(K).ljust(11) + "  " + str(L).ljust(
                        2) + "  " + str(M).ljust(14) + "  " + str(N).ljust(2) + " " + str(O).ljust(2) + str(P).ljust(
                        1) + str(Q).ljust(1) + str(R).ljust(1) + str(S).ljust(3) + str(T).ljust(1) + str(U).ljust(
                        4) + str(V).ljust(1) + str(W).ljust(1) + str(ESPECIAL).ljust(2) + " " + str(X).ljust(
                        8) + " " + str(Y).ljust(1) + "\n")


# Generamoos una clase donde especificamos que se debe de hacer cuando se genera un fichero en el directorio a monitorear. Solo procesa fichero .marl
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Este código define un método on_created que se llama cuando se crea un fichero. Si el elemento creado es un directorio, no devuelve nada y no se llama a ninguna funcion adicional.
        Si el elemento creado es un archivo .marl, llama a una función procesar_archivo con la ruta del archivo creado como argumento.
        """
        if event.is_directory:
            return
        if event.src_path.endswith('.marl'):
            procesar_archivo(event.src_path)


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
