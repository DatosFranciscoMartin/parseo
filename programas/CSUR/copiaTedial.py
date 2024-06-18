import tkinter as tk
from tkinter import messagebox
import shutil
import os


def convert_path(local_path):
    base_network_path = r"Y:\Tedial"
    relative_path = local_path.replace("/storage/MANAGED", "").replace("/", "\\")
    network_path = base_network_path + relative_path
    return network_path


def get_new_filename(local_path):
    # Extraer el nombre del archivo sin la ruta ni extensión.
    filename = os.path.basename(local_path)
    new_filename = filename.split('_')[0] + ".mxf"
    return new_filename


def copy_and_rename_file():
    source = source_entry.get()  # Obtiene la ruta de origen ingresada por el usuario
    network_source = convert_path(source)  # Convierte la ruta a la ruta de red correspondiente
    destination_dir = destination_entry.get()  # Obtiene la ruta de destino predefinida
    new_filename = get_new_filename(source)  # Obtiene el nuevo nombre del archivo
    destination = os.path.join(destination_dir,
                               new_filename)  # Combina la ruta de destino y el nuevo nombre del archivo

    if not os.path.exists(network_source):
        messagebox.showerror("Error", "La ruta de origen en la red no existe")
        return

    # Verifica si el directorio de destino existe, si no, lo crea
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    try:
        shutil.copy(network_source, destination)
        messagebox.showinfo("Éxito", "Copia y renombrado completado con éxito")
    except Exception as e:
        messagebox.showerror("Error", f"Error al copiar y renombrar: {e}")


# Crear la ventana principal
root = tk.Tk()
root.title("Copiar y Renombrar Archivo")

# Ruta de destino por defecto
default_destination = r"W:\entrada"

# Crear y colocar los widgets
tk.Label(root, text="Ruta de Origen:").grid(row=0, column=0, padx=10, pady=10)
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Ruta de Destino:").grid(row=1, column=0, padx=10, pady=10)
destination_entry = tk.Entry(root, width=50)
destination_entry.insert(0, default_destination)  # Inserta la ruta por defecto
destination_entry.grid(row=1, column=1, padx=10, pady=10)
destination_entry.config(state='readonly')  # Hace que el campo de destino sea de solo lectura

tk.Button(root, text="Copiar y Renombrar", command=copy_and_rename_file).grid(row=2, column=1, pady=20)

# Iniciar el bucle principal de la interfaz
root.mainloop()
