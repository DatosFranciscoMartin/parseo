import os
import shutil

def espejo_carpeta(origen, destino):
    # Si el directorio de destino no existe, lo creamos
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Iteramos sobre los elementos en la carpeta de origen
    for elemento in os.listdir(origen):
        ruta_origen = os.path.join(origen, elemento)
        ruta_destino = os.path.join(destino, elemento)

        # Si es un directorio, llamamos recursivamente a la función
        if os.path.isdir(ruta_origen):
            espejo_carpeta(ruta_origen, ruta_destino)
        else:
            # Si es un archivo, lo copiamos
            shutil.copy2(ruta_origen, ruta_destino)

    # Para eliminar archivos que ya no están en la carpeta de origen
    for elemento in os.listdir(destino):
        ruta_destino = os.path.join(destino, elemento)
        ruta_origen = os.path.join(origen, elemento)
        if not os.path.exists(ruta_origen):
            if os.path.isdir(ruta_destino):
                shutil.rmtree(ruta_destino)  # Eliminar directorio
            else:
                os.remove(ruta_destino)  # Eliminar archivo

# Ejemplo de uso
origen = (r'Z:\emision')  # Cambia esto por la ruta de la carpeta de origen
destino = (r'M:\')  # Cambia esto por la ruta de la carpeta de destino
espejo_carpeta(origen, destino)

print("El espejo de la carpeta se ha creado.")
