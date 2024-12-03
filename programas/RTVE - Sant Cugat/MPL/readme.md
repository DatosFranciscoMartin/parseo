# Script para el parseo de ficheros TRF a XML crear_xml.py

Este script de Python está diseñado para procesar archivos TRF y generar archivos XML de tipo Marina Playlist (MPL) basados en la información contenida en los archivos TRF.

## Funcionalidades Principales:

1. Selección de Archivos y Directorio de Salida:

    * Al ejecutar el script, se abrirá una ventana que permite al usuario seleccionar múltiples archivos TRF.
    * También se puede elegir un directorio de salida donde se guardarán los archivos XML generados.

2. Procesamiento de Archivos TRF:

    * El script procesa los archivos TRF seleccionados y extrae la información relevante para la generación de archivos XML.
    * Se utilizan técnicas de manipulación de archivos y cadenas de texto para extraer datos específicos de cada archivo TRF.

3. Generación de Archivos XML MPL:

    * Basándose en la información extraída de los archivos TRF, el script genera archivos XML MPL que siguen el estándar requerido.
    * Los archivos XML MPL contienen información sobre los eventos programados, como eventos en vivo, comentarios y segmentos de video.

### Requisitos:

* Python 3.x
* Librerías estándar de Python (xml.etree.ElementTree, xml.dom.minidom, os, datetime, tkinter, logging)

### Uso:

1. Ejecutar el script.
2. mSeleccionar los archivos TRF deseados.
3. Elegir un directorio de salida para los archivos XML generados.
4. El script procesará los archivos TRF y generará archivos XML MPL en el directorio especificado.

### Notas Adicionales:

* Los archivos XML MPL generados seguirán el formato requerido para su uso en el sistema correspondiente.
* Se proporcionan comentarios detallados en el código para facilitar la comprensión y la modificación según sea necesario.

# Código de Monitoreo y Procesamiento de Archivos TRF crear_xml_watcher.py
Este es un script de Python diseñado para monitorear un directorio específico en busca de archivos con extensión ".trf" o ".TRF". Cuando se detecta la creación de un archivo en este directorio, el script procesa automáticamente el archivo, extrae información relevante y genera un archivo XML correspondiente.

## Requisitos Previos
Asegúrese de tener instaladas las siguientes bibliotecas de Python antes de ejecutar el script:

* tkinter: Utilizado para la interfaz gráfica de usuario (GUI) para seleccionar directorios.
* watchdog: Utilizado para monitorear cambios en los archivos del directorio.
* xml.etree.ElementTree: Utilizado para generar y manipular documentos XML.
* xml.dom.minidom: Utilizado para formatear el documento XML generado.
* datetime: Utilizado para manejar fechas y tiempos.
* logging: Utilizado para generar registros (logs) del proceso.

Puede instalar estas bibliotecas utilizando pip:

```python
pip install tk watchdog
```

## Instrucciones de Uso

1. Ejecute el script Python.
2. Se abrirá una ventana de interfaz gráfica.
3. Seleccione el directorio que desea monitorear y el directorio de salida donde se generarán los archivos XML resultantes haciendo clic en los botones correspondientes.
4. Una vez seleccionados los directorios, haga clic en el botón "Ejecutar" para iniciar el monitoreo.
5. El script comenzará a monitorear el directorio seleccionado en busca de archivos ".trf" o ".TRF".
6. Cuando se cree un archivo en el directorio monitoreado, el script lo procesará automáticamente y generará un archivo XML correspondiente en el directorio de salida especificado.

## Funcionamiento del Script
* El script utiliza la biblioteca watchdog para monitorear cambios en el directorio especificado.
* Cuando se detecta la creación de un archivo en el directorio, se utiliza la biblioteca xml.etree.ElementTree para procesar el archivo y extraer información relevante.
* La información extraída se utiliza para generar un documento XML que cumple con un formato específico.
* Los archivos XML generados se guardan en el directorio de salida especificado.
* El script también registra eventos y errores en un archivo de registro para facilitar el seguimiento y la depuración.