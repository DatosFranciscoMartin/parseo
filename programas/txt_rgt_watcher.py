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
    Este fragmento de código Python define una función procesar_archivo que procesa un archivo txt. Extrae información del archivo de entrada, manipula los datos y escribe la salida formateada en un nuevo archivo. 
    El código incluye operaciones como la lectura de líneas específicas, la extracción de subcadenas y la escritura de datos formateados en un archivo de salida. 
    También registra el nombre del fichero procesado e imprime un mensaje en la consola.
    """
    # Generamos el nombre del fichero para el log, eliminamos la ruta absoluta y nos quedamos solo con el nombre del fichero
    nombre_archivo = os.path.basename(archivo)
    logging.info(f"Archivo procesado: {nombre_archivo}")

    #Mensaje en la consola de salida que se indica que fichero se esta procesando.

    print("Procesando archivo:", archivo)

    # Abre cada archivo en modo lectura
    with open(archivo, "r", encoding="iso-8859-1") as fichero:
        # Lee las primeras líneas que quieres omitir
        for _ in range(2):
            next(fichero)

        # Lee la siguiente línea que contiene información necesaria
        linea_circuito = fichero.readline()
        circuito = linea_circuito[10:13]

        linea_fecha = fichero.readline()
        year = linea_fecha[12:14]
        mes = linea_fecha[9:11]
        dia = linea_fecha[6:8]

        # Abre el archivo de salida en el directorio seleccionado
        # Se crea el fichero en modo escritura bajo el encode utf-8
        with open(os.path.join(directorio_salida, f"{circuito}{year}{mes}{dia}.rgt"), "w", encoding="iso-8859-1") as Archivo_salida:
            Archivo_salida.write(circuito+year+mes+dia+"\n")


            # Otras operaciones para leer el archivo y escribir en el archivo de salida
            for _ in range(4):
                next(fichero)

            for linea in fichero:
                # Realiza operaciones en cada línea del archivo y escribe en el archivo de salida
                # Formato fichero

                TYPE = linea[1:6]
                START_TIME = linea[6:29]
                END_TIME = linea[29:52]
                MEDIA_ID = linea[52:85]
                EVENT = linea[85:106]
                TITLE = linea[106:139]
                SOM = linea[139:151]
                SEGMENT = linea[151:184]
                DURATION = linea[184:196]
                START_TYPE = linea[196:209]
                STRT_OFFSET = linea[209:221]
                END_TYPE = linea[221:234]
                END_OFFSET = linea[234:246]
                DEVICE_STREAM = linea[246:279]
                RECONCILE_KEY = linea[279:312]
                HOUSE_ID = linea[312:345]
                STATUS = linea[345:371]
                DEFAULT = "                                                                    "

                # Comprobamos que sea media Event y el status no sea missed
                if EVENT == "Media Event          " and STATUS != "Missed                    ":
                    # Iteramos sobre cada carácter en la cadena
                    for caracter in RECONCILE_KEY:
                        # Ignoramos los espacios en blanco
                        if caracter == " ":
                            # Incrementamos el recuento para el carácter actual
                            RECONCILE_KEY = " " * 27
                            break

                    A = START_TIME[11:22]
                    B = MEDIA_ID[:18]
                    C = DEFAULT[:2]
                    D = TITLE[:32]
                    E = DURATION[:11]
                    F = RECONCILE_KEY[3:4]
                    G = RECONCILE_KEY[1:2]
                    if G == " " or G == "0":
                        G = "2"
                    H = RECONCILE_KEY[4:11]
                    I = RECONCILE_KEY[11:14]
                    J = DEFAULT[:5]
                    K = RECONCILE_KEY[14:25]
                    L = RECONCILE_KEY[25:27]
                    M = DEFAULT[:14]
                    N = DEFAULT[:2]
                    O = DEFAULT[:2]
                    P = RECONCILE_KEY[0:1]
                    if P == " " or P == "0":
                        P = "7"
                    Q = DEFAULT[:1]
                    R = RECONCILE_KEY[2:3]
                    S = DEFAULT[:3]
                    if S == "   ":
                        S = "EST"
                    T = DEFAULT[:1]
                    U = DEFAULT[:4]
                    V = DEFAULT[:1]
                    W = DEFAULT[:1]
                    ESPECIAL = DEFAULT[:2]
                    X = RECONCILE_KEY[28:]
                    # Iteramos sobre cada carácter en la cadena
                    for caracter in X:
                        # Ignoramos los espacios en blanco
                        if caracter == " ":
                            break
                        else:
                            X = X+":00"
                            break

                    Y = DEFAULT[:1]

                    # Escribimos en el archivo de salida la línea formateada correctamente.
                    Archivo_salida.write(f"{A}  {B}  {C}  {D}  {E}  {F} {G}{H}  {I}  {J}  {K}  {L}  {M}  {N} {O}{P}{Q}{R}{S}{T}{U}{V}{W}{ESPECIAL} {X} {Y}\n")

                    

# Generamoos una clase donde especificamos que se debe de hacer cuando se genera un fichero en el directorio a monitorear. Solo procesa fichero .txt
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Este código define un método on_created que se llama cuando se crea un fichero. Si el elemento creado es un directorio, no devuelve nada y no se llama a ninguna funcion adicional. 
        Si el elemento creado es un archivo .txt, llama a una función procesar_archivo con la ruta del archivo creado como argumento.
        """
        if event.is_directory:
            return
        if event.src_path.endswith('.txt'):
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
