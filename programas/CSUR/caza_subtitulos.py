import os
import shutil
import time
import pyodbc
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
from datetime import datetime

class CazadorSubtitulosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cazador de Subtítulos en FileCatalyst")

        self.origenes = []

        self.label_entrada = tk.Label(root, text="Carpetas de entrada:")
        self.label_entrada.pack()

        self.frame_lista = tk.Frame(root)
        self.frame_lista.pack()

        self.lista_origenes = Listbox(self.frame_lista, selectmode=tk.SINGLE, width=60, height=6)
        self.lista_origenes.pack(side=tk.LEFT)

        self.scrollbar = Scrollbar(self.frame_lista, orient=tk.VERTICAL, command=self.lista_origenes.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_origenes.config(yscrollcommand=self.scrollbar.set)

        self.boton_agregar = tk.Button(root, text="Agregar carpeta de entrada", command=self.agregar_origen)
        self.boton_agregar.pack(pady=5)

        self.boton_quitar = tk.Button(root, text="Quitar carpeta seleccionada", command=self.quitar_origen)
        self.boton_quitar.pack()

        self.label_salida = tk.Label(root, text="Carpeta de salida:")
        self.label_salida.pack(pady=(10, 0))

        self.entry_destino = tk.Entry(root, width=60)
        self.entry_destino.pack()

        self.boton_seleccionar_destino = tk.Button(root, text="Seleccionar carpeta de salida", command=self.seleccionar_destino)
        self.boton_seleccionar_destino.pack(pady=5)

        self.boton_iniciar = tk.Button(root, text="Iniciar procesamiento", command=self.iniciar)
        self.boton_iniciar.pack(pady=10)

        self.destino = ""

    def agregar_origen(self):
        carpeta = filedialog.askdirectory(title="Selecciona una carpeta de entrada")
        if carpeta and carpeta not in self.origenes:
            self.origenes.append(carpeta)
            self.lista_origenes.insert(tk.END, carpeta)

    def quitar_origen(self):
        seleccion = self.lista_origenes.curselection()
        if seleccion:
            index = seleccion[0]
            self.lista_origenes.delete(index)
            del self.origenes[index]

    def seleccionar_destino(self):
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta de salida")
        if carpeta:
            self.destino = carpeta
            self.entry_destino.delete(0, tk.END)
            self.entry_destino.insert(0, carpeta)

    def iniciar(self):
        if not self.origenes:
            messagebox.showerror("Error", "Debes agregar al menos una carpeta de entrada.")
            return
        if not self.destino:
            messagebox.showerror("Error", "Debes seleccionar una carpeta de salida.")
            return

        messagebox.showinfo("Procesando", "El proceso comenzará y se repetirá cada 5 minutos. Cierra la consola para detenerlo.")
        self.root.destroy()
        ejecutar_proceso_en_bucle(self.origenes, self.destino)

def ejecutar_proceso_en_bucle(origenes, destino):
    log_path = os.path.join(destino, "registro.txt")
    sub_diario = "S:\\"

    try:
        while True:
            # Limpiar el log: mantener solo las últimas 1000 líneas
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    lineas = f.readlines()[-1000:]
                with open(log_path, "w", encoding="utf-8") as f:
                    f.writelines(lineas)

            # Agregar nueva ejecución
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"\n--- EJECUCIÓN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

                for origen_base in origenes:
                    cazar_subtitulos(origen_base, destino, log_file)

                mover_subtitulos(destino, sub_diario, log_file)

            # Cuenta atrás de 5 minutos
            total_segundos = 300
            print("Esperando 5 minutos para la siguiente ejecución...")
            for restante in range(total_segundos, 0, -1):
                mins, secs = divmod(restante, 60)
                tiempo_str = f"{mins:02d}:{secs:02d}"
                print(f"\rTiempo restante: {tiempo_str}", end="", flush=True)
                time.sleep(1)
            print("\n")
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")

def cazar_subtitulos(origen_base, destino, log_file):
    origen = os.path.join(origen_base, "storage", "Para_CanalSur")
    if not os.path.exists(origen):
        msg = f"[AVISO] No existe la ruta: {origen}"
        print(msg)
        log_file.write(msg + "\n")
        return

    otros = os.path.join(destino, "otros")
    os.makedirs(otros, exist_ok=True)

    print(f"\nCazando en: {origen}")
    log_file.write(f"\n****CAZANDO EN: {origen}****\n")

    for archivo in os.listdir(origen):
        if not archivo.lower().endswith(".stl"):
            continue

        nombre_archivo = archivo
        archivo_sin_ext, extension = os.path.splitext(archivo)

        base_nombre = None

        if archivo_sin_ext.isdigit() and len(archivo_sin_ext) == 10:
            base_nombre = archivo_sin_ext
        elif archivo_sin_ext.startswith("HD") and archivo_sin_ext[2:].isdigit() and len(archivo_sin_ext) == 12:
            base_nombre = archivo_sin_ext[2:]
        else:
            ruta_archivo_origen = os.path.join(origen, archivo)

            ruta_archivo_destino_otros = os.path.join(otros, nombre_archivo)

            shutil.move(ruta_archivo_origen, ruta_archivo_destino_otros)
            msg = f'[ERROR] Nombre inválido, archivo "{nombre_archivo}" movido a carpeta "otros".'
            print(msg)
            log_file.write(msg + "\n")
            continue

        carpeta = base_nombre[:7] + "000"
        ruta_carpeta = os.path.join(destino, carpeta)
        ruta_archivo_destino = os.path.join(ruta_carpeta, nombre_archivo)
        ruta_archivo_origen = os.path.join(origen, archivo)

        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            msg = f"[INFO] Carpeta creada: {ruta_carpeta}"
            print(msg)
            log_file.write(msg + "\n")

        if os.path.exists(ruta_archivo_destino):
            msg = f'[AVISO] Archivo ya existe: "{ruta_archivo_destino}". No se movió el archivo "{nombre_archivo}".'
            print(msg)
            log_file.write(msg + "\n")
        else:
            shutil.move(ruta_archivo_origen, ruta_carpeta)
            msg = f'Archivo "{nombre_archivo}" movido a "{ruta_carpeta}"'
            print(msg)
            log_file.write(msg + "\n")


def mover_subtitulos(repo_sub, sub_diario, log_file):
    # Parámetros de conexión
    server = '10.236.174.70'  # IP o nombre del servidor SQL remoto
    database = 'CanalSur_AutomationDB'
    username = 'pbsdbviewer'
    password = 'pbsdbviewer'
    driver = 'ODBC Driver 17 for SQL Server'  # O el que tengas disponible

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT [MediaName]
            FROM [dbo].[taListMediaUsage]
            WHERE [MediaTypeId] = '2'
        """)

        lista_subtitulos = set()
        msg = "\n****RECUPERANDO ARCHIVOS DE SUBTITULOS****\n"
        print(msg)
        log_file.write(msg + "\n")

        for row in cursor.fetchall():
            lista_subtitulos.add(row.MediaName + ".stl")
            media_name = row.MediaName + ".stl"
            encontrado = False

            if row.MediaName.startswith("HD"):
                carpeta_busqueda = row.MediaName[2:9] + "000"
            elif row.MediaName.startswith("0"):
                carpeta_busqueda = row.MediaName[:7] + "000"

            path_busqueda = os.path.join(repo_sub, carpeta_busqueda, media_name)
            ruta_alternativa = os.path.join(repo_sub, "otros", media_name)

            if not os.path.exists(os.path.join(sub_diario, media_name)):
                try:
                    shutil.copy2(path_busqueda, sub_diario)
                    msg = f"[+] Archivo {media_name} copiado"
                    print(msg)
                    log_file.write(msg + "\n")
                except FileNotFoundError:
                    msg = f"[-] Archivo {media_name} no encontrado. Intentando copia desde ruta alternativa..."
                    print(msg)
                    log_file.write(msg + "\n")
                    try:
                        if not os.path.exists(os.path.join(sub_diario, media_name)):
                            shutil.copy2(ruta_alternativa, sub_diario)
                            msg = f"[+] Archivo {media_name} copiado desde ruta alternativa"
                            print(msg)
                            log_file.write(msg + "\n")
                    except Exception as e:
                        msg = f"          Tampoco se pudo copiar desde la ruta alternativa: {e}"
                        print(msg)
                        log_file.write(msg + "\n")
            else:
                msg = f"[AVISO] Archivo ya existe en destino: {media_name}. No se copió."
                print(msg)
                log_file.write(msg + "\n")

        lista_subtitulos = set()
        msg = "\n****LIMPIANDO CARPETA DE SUBTITULOS****\n"
        print(msg)
        log_file.write(msg + "\n")

        for listado in os.listdir(sub_diario):
            ruta_archivo = os.path.join(sub_diario, listado)

            # 3. Si no está en la lista válida, lo eliminamos
            if listado not in lista_subtitulos and os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
                msg = f"Archivo eliminado: {listado}"
                print(msg)
                log_file.write(msg + "\n")

    except pyodbc.Error as e:
        msg = f"Error de conexión o consulta: {e}"
        print(msg)
        log_file.write(msg + "\n")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CazadorSubtitulosApp(root)
    root.mainloop()
