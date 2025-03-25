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

def obtener_datos_nodo(servers):
    datos = {}

    for nombre_nodo, ip_nodo in servers.items():
        urls = {
            "senders": f"http://{ip_nodo}/x-nmos/connection/v1.1/single/senders/",
            "receivers": f"http://{ip_nodo}/x-nmos/connection/v1.1/single/receivers/"
        }

        datos[nombre_nodo] = {"senders": [], "receivers": []}

        for tipo, url in urls.items():
            if tipo == "senders":
                try:
                    response = requests.get(url, timeout=5)
                    datos[nombre_nodo][tipo] = response.json()
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
                datos[nombre_nodo][tipo] = {"error": mensaje_error}
                logging.error(f"{mensaje_error} al servidor: {nombre_nodo}, no se ha podido obtener los senders")
                
            elif tipo == "receivers":
                try:
                    response = requests.get(url, timeout=5)
                    datos[nombre_nodo][tipo] = response.json()
                except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
                    mensaje_error = "URL no válida"
                except requests.exceptions.ConnectionError:
                    mensaje_error = "Error de conexión"
                except requests.exceptions.Timeout:
                    mensaje_error = "Tiempo de espera agotado"
                except requests.exceptions.RequestException as e:
                    mensaje_error = f"Error desconocido: {e}"
                else:
                    continue

                # Si hubo error, almacénalo en el diccionario y regístralo en logs
                datos[nombre_nodo][tipo] = {"error": mensaje_error}
                logging.error(f"{mensaje_error} al servidor: {nombre_nodo}, no se ha podido obtener los receivers")

    return datos

try:
    config_path = r'C:\Users\franciscojavier.mart\Documents\Repos\parseo\programas\NMOS\Discovery\cf\config.conf'
    configuration = load_config(config_path)
    # Acceso a los servidores
    servers = configuration.get('Maquinas', {}).get('servers', {})
    logging.info(f"Servidores configurados: {servers}")
except Exception as e:
    logging.error(f"No se pudo cargar la configuración: {str(e)}")

datos = obtener_datos_nodo(servers)

datos_formateado = json.dumps(datos, indent=4)
print(datos_formateado)