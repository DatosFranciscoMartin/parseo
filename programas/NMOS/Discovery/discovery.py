from configparser import ConfigParser
import os
import requests
import json
import logging
from ast import literal_eval

# Obtener el directorio actual donde se ejecuta el script
current_directory = os.path.dirname(os.path.abspath(__file__))

#Generar el fichero de log en el directorio donde se ejecuta el script
if not current_directory + "/registro.log":
    log_file_path = os.path.join(current_directory, 'registro.log')
else:
    log_file_path = current_directory + "/registro.log"

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,  # Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
    handlers=[
        logging.FileHandler(log_file_path),  # Archivo de log
        logging.StreamHandler()  # También imprimir en consola
    ]
)

# Funcion que vamos a usar para parsear la informacion del fichero de configuracion
def parse_custom_config(filepath):
    """
    Parsea archivos de configuración con formato especial para la sección [Maquinas]
    """


    # Iniciamos el diccionario de configuracion donde vamos a guardar los datos del fichero de configuracion
    config = {}
    try:
        # Primero intentamos con configparser estándar
        parser = ConfigParser()
        parser.read(filepath)
        if 'Maquinas' in parser:
            try:
                # Intentamos evaluar el contenido como diccionario Python
                servers_str = parser['Maquinas'].get('servers', '{}')
                config['Maquinas'] = {
                    'servers': literal_eval(servers_str)
                }
            except (SyntaxError, ValueError) as e:
                logging.error(f"Error parseando servidores: {str(e)}")
        return config
    except Exception as e:
        logging.exception(f"Error procesando archivo de configuración: {str(e)}")
        raise

# Funcion con la que vamos a cargar las configuraciones de los servidores
def load_config(filepath):
    """Carga y valida el archivo de configuración"""
    if not os.path.exists(filepath):
        logging.error(f"Archivo no encontrado: {filepath}")
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {filepath}")
    
    try:
        config = parse_custom_config(filepath)
        logging.info("Configuración cargada exitosamente")
        logging.debug(f"Configuración parseada: {config}")
        return config
    except json.JSONDecodeError:
        logging.error("El formato JSON de los servidores es inválido")
        raise
    except Exception as e:
        logging.error(f"Error inesperado al cargar configuración: {str(e)}")
        raise

# Funcion en la que vamos a realizar consultas a los servidores que hayamos puesto en el fichero configuracion
def obtener_datos_nodo(servers):

    # Cargamos el diccionario donde vamos a guardar los datos de los senders y receivers de los servidores que ser hayan cargado en la configuracion
    datos = {}

    # Recorremos el diccionario de servidores para buscar la ip o el nombre del servidor y obtener los senders y receivers de cada uno de ellos
    for nombre_nodo, ip_nodo in servers.items():
        urls = {
            "senders": f"http://{ip_nodo}/x-nmos/connection/v1.1/single/senders/",
            "receivers": f"http://{ip_nodo}/x-nmos/connection/v1.1/single/receivers/"
        }

        # Le damos formato al diccionario con los senders y receivers
        datos[nombre_nodo] = {"senders": [], "receivers": []}

        # Intentamos obtener los senders y receivers de cada servidor haciendo consultas
        for tipo, url in urls.items():
            # Tipo sender
            if tipo == "senders":
                try:
                    # Realizamos la consulta tipo get de los senders
                    response = requests.get(url, timeout=5)
                    datos[nombre_nodo][tipo] = response.json()
                # Manejamos las posibles excepciones
                except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
                    mensaje_error = "URL no válida"
                except requests.exceptions.ConnectionError:
                    mensaje_error = "Error de conexión"
                except requests.exceptions.Timeout:
                    mensaje_error = "Tiempo de espera agotado"
                except requests.exceptions.RequestException as e:
                    mensaje_error = f"Error desconocido: {e}"
                else:
                    continue  # Si no hubo errores, pasa al siguiente
                # Si hubiera algun error al obtener los datos en la consulta, creamos un diccionario con el error y lo almacenamos, tambien lo guardamos en el log
                datos[nombre_nodo][tipo] = {"error": mensaje_error}
                logging.error(f"{mensaje_error} al servidor: {nombre_nodo}, no se ha podido obtener los senders")
            
            # Tipo receiver
            elif tipo == "receivers":
                try:
                    # Realizamos la consulta tipo get de los receiver
                    response = requests.get(url, timeout=5)
                    datos[nombre_nodo][tipo] = response.json()
                # Manejamos las posibles excepciones
                except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
                    mensaje_error = "URL no válida"
                except requests.exceptions.ConnectionError:
                    mensaje_error = "Error de conexión"
                except requests.exceptions.Timeout:
                    mensaje_error = "Tiempo de espera agotado"
                except requests.exceptions.RequestException as e:
                    mensaje_error = f"Error desconocido: {e}"
                else:
                    continue # Si no hubiera errores, continua

                # Si hubiera algun error al obtener los datos en la consulta, creamos un diccionario con el error y lo almacenamos, tambien lo guardamos en el log
                datos[nombre_nodo][tipo] = {"error": mensaje_error}
                logging.error(f"{mensaje_error} al servidor: {nombre_nodo}, no se ha podido obtener los receivers")

    # Devolvermos el diccionario con los datos que hemos conseguido
    return datos

####################################################################################################################################################################
######################################################                                                    ##########################################################
###################################################   A PARTIR DE ESTE PUNTO TENEMOS EL PROGRAMA PRINCIPAL      ####################################################
######################################################                                                    ##########################################################
####################################################################################################################################################################


try:
    # Cargamos el fichero de configuracion en la ruta que nosotros le indiquemos
    #config_path = r'C:\Users\franciscojavier.mart\Documents\Repos\parseo\programas\NMOS\Discovery\cf\config.conf'
    config_path = r'/root/nmos/NMOS/Discovery/cf/config.conf'
    # Usamos la funcion para cargar la configuracion 
    configuration = load_config(config_path)
    # Cargamos la configuracion del fichero en una variable para procesarla
    servers = configuration.get('Maquinas', {}).get('servers', {})
    logging.info(f"Servidores configurados: {servers}")
except Exception as e:
    logging.error(f"No se pudo cargar la configuración: {str(e)}")

# Cargamos la salida
datos = obtener_datos_nodo(servers)

datos_formateado = json.dumps(datos, indent=4)
print(datos_formateado)