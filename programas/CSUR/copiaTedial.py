import tkinter as tk
from tkinter import messagebox, ttk
import os
import time


def convert_path(local_path):
    base_network_path = r"Y:\Tedial"
    relative_path = local_path.replace("/storage", "").replace("/", "\\")
    network_path = base_network_path + relative_path
    return network_path


def get_new_filename(local_path):
    filename = os.path.basename(local_path)
    new_filename = filename.split('_')[0] + ".mxf"
    return new_filename


def copy_and_rename_file():
    source = source_entry.get()
    network_source = convert_path(source)
    destination_dir = destination_entry.get()
    new_filename = get_new_filename(source)
    destination = os.path.join(destination_dir, new_filename)

    if not os.path.exists(network_source):
        messagebox.showerror("Error", "La ruta de origen en la red no existe")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    try:
        copy_file_with_progress(network_source, destination)
        messagebox.showinfo("Éxito", "Copia y renombrado completado con éxito")
    except Exception as e:
        messagebox.showerror("Error", f"Error al copiar y renombrar: {e}")


def copy_file_with_progress(source, destination):
    chunk_size = 1024 * 1024  # 1MB
    total_size = os.path.getsize(source)
    copied_size = 0

    progress_bar['maximum'] = total_size

    start_time = time.time()

    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dst.write(chunk)
            copied_size += len(chunk)
            progress_bar['value'] = copied_size
            root.update_idletasks()

            elapsed_time = time.time() - start_time
            speed = copied_size / (1024 * 1024 * elapsed_time)  # MB/s
            speed_label.config(text=f"Velocidad: {speed:.2f} MB/s")

        progress_bar['value'] = total_size
        speed_label.config(text=f"Velocidad: {speed:.2f} MB/s")
        root.update_idletasks()


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
destination_entry.insert(0, default_destination)
destination_entry.grid(row=1, column=1, padx=10, pady=10)
destination_entry.config(state='readonly')

tk.Button(root, text="Copiar y Renombrar", command=copy_and_rename_file).grid(row=2, column=1, pady=20)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

speed_label = tk.Label(root, text="Velocidad: 0.00 MB/s")
speed_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()
