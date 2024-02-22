# parseo
Programa para el parseo de ficheros de marina

# Programa para la generación de ficheros rgt **txt_rgt.py**

En el programa llamado **txt_rgt.py** tenemos un programa que parsea un fichero **.txt** con un formato determinado (se pueden comprobar algunos ejemplos de ficheros **.txt** en la carpeta *Asrun Marina*) el fichero resultante es un archivo formateado de extensión **.rgt**

## Instrucciones de uso

1. Ejecute el script txt_rgt.py.
2. Haga clic en el botón "Seleccionar archivos" para elegir los archivos que desea procesar.
3. Haga clic en el botón "Seleccionar directorio de salida" para elegir el directorio donde se guardarán los archivos procesados.
4. Una vez seleccionados los archivos y el directorio de salida, haga clic en el botón "Ejecutar" para procesar los archivos y generar los archivos de salida.
5. Los archivos procesados se guardarán en el directorio seleccionado.
6. El programa también generará un archivo de registro (archivo_log.log) en el directorio de salida, que contiene información sobre los archivos procesados.

### Requisitos
* cPython 3.x
* mTkinter (instalado por defecto en la mayoría de las distribuciones de Python)

### Notas
* Asegúrese de tener permisos de escritura en el directorio de salida seleccionado.
* Este programa ha sido probado en sistemas Windows y Linux.

# script de monitorización de directorios y procesamiento de archivos **txt_rgt_watcher.py**

Este script de Python proporciona una interfaz gráfica de usuario (GUI) para seleccionar directorios a monitorizar y directorios de salida, además de implementar funcionalidades para monitorear cambios en archivos de texto (.txt) en el directorio seleccionado y procesarlos en archivos de salida con un formato específico.

## Funcionalidades principales

1. Selección de directorios:
    * Los usuarios pueden seleccionar un directorio para monitorizar archivos y otro directorio para almacenar los archivos procesados como salida.

2. Monitorización de directorios:
    * El script utiliza la librería watchdog para monitorear el directorio seleccionado en busca de cambios en los archivos. Cuando se detecta la creación de un nuevo archivo, el script lo procesa automáticamente.

3. Procesamiento de archivos:
    * Los archivos de texto creados en el directorio monitorizado se procesan según un formato específico, extrayendo información relevante y escribiendo la salida formateada en archivos nuevos en el directorio de salida seleccionado.

## Instrucciones de uso

1. Instalación de dependencias:

    * Es necesario tener instaladas las siguientes librerías de Python:
        * tkinter: Para la interfaz gráfica.
        * watchdog: Para monitorear cambios en los directorios.

2. Ejecución del script:

    * Al ejecutar el script, se abrirá una ventana de GUI donde podrás seleccionar los directorios a monitorizar y de salida. Después de seleccionarlos, puedes iniciar la monitorización haciendo clic en el botón "Ejecutar".

3. Procesamiento de archivos:

    * Cuando se crea un nuevo archivo de texto (.txt) en el directorio monitorizado, el script lo procesa automáticamente y escribe la salida formateada en el directorio de salida.

### Consideraciones adicionales

* Formato de archivos de salida:

    Los archivos de salida siguen un formato específico determinado por el contenido de los archivos de entrada. La información se extrae y se escribe en un nuevo archivo de salida con un nombre que refleja la fecha y hora de procesamiento.

* Registro de eventos:

    El script genera un registro en tiempo real de los eventos de procesamiento en un archivo de registro. Este registro contiene información sobre los archivos procesados y se almacena en el directorio de salida.

### Notas finales

Este script proporciona una manera eficiente de monitorear directorios en busca de nuevos archivos y procesarlos automáticamente según un formato definido. Puede ser útil en situaciones donde se requiere procesamiento automático de archivos en tiempo real, como en sistemas de registro o análisis de datos continuo.

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









