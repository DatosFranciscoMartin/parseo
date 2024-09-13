import configparser
import logging
import os

def procesar_etb():
    """
    Funcion donde vamos a procesar el fichero XML que viene desde Neptune para hacer el parseo a Automation.
    """

    # Obtener el directorio actual donde se ejecuta el script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(current_directory, 'log.log')
    #print(f'El archivo de log se generará en: {log_file_path}')

    # Configurar el logger
    logging.basicConfig(
        level=logging.INFO,  # Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
        handlers=[
            logging.FileHandler(log_file_path),  # Archivo de log
            logging.StreamHandler()  # También imprimir en consola
        ]
    )

    configuracion = configparser.ConfigParser()

    # Leer el archivo de configuración
    try:
        if os.path.exists(r'D:\Traductor\Ejecutor\cf\config.conf'):
            configuracion.read(r'D:\Traductor\Ejecutor\cf\config.conf')
        elif os.path.exists(r'C:\Users\franciscojavier.mart\Documents\parseo\programas\ETB\c\config.conf'):
            configuracion.read(r'C:\Users\franciscojavier.mart\Documents\parseo\programas\ETB\cf\config.conf')
        else:
            logging.error('Archivo de configuración no encontrado en ninguna de las rutas especificadas.')
            #raise FileNotFoundError('No se encontró el archivo de configuración.')
    except Exception as e:
        logging.exception('Error al leer el archivo de configuración: %s', e)

procesar_etb()
