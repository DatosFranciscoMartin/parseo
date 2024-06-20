import os
import time


def get_files_sizes(folder):
    """Obtiene los tamaños de los archivos en la carpeta dada."""
    files_sizes = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            files_sizes[file_path] = os.path.getsize(file_path)
    return files_sizes


def calculate_growth_rate(initial_sizes, final_sizes, interval):
    """Calcula la tasa de crecimiento de los archivos."""
    growth_rates = {}
    for file_path in final_sizes:
        if file_path in initial_sizes:
            initial_size = initial_sizes[file_path]
            final_size = final_sizes[file_path]
            growth = final_size - initial_size
            rate = growth / interval  # bytes per second
            if growth > 0:  # Consider only growing files
                growth_rates[file_path] = rate
    return growth_rates


def monitor_folder_growth(folder, interval=60):
    """Monitorea el crecimiento de archivos en una carpeta durante un intervalo."""
    print(f"Monitoring folder: {folder}")
    initial_sizes = get_files_sizes(folder)
    print("Initial file sizes captured.")
    time.sleep(interval)
    final_sizes = get_files_sizes(folder)
    print("Final file sizes captured.")

    growth_rates = calculate_growth_rate(initial_sizes, final_sizes, interval)

    if growth_rates:
        print("\nFiles that grew and their growth rates (bytes/second):")
        for file_path, rate in growth_rates.items():
            print(f"{file_path}: {rate:.2f} bytes/second")
    else:
        print("\nNo files grew during the monitoring period.")


if __name__ == "__main__":
    folder_to_monitor = "W:\emision"  # Reemplaza esto con la ruta a la carpeta que deseas monitorear
    monitor_folder_growth(folder_to_monitor)
