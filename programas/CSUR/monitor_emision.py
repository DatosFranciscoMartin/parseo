import os
import time
import tkinter as tk
from tkinter import ttk, scrolledtext


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


def monitor_folder_growth(folder, interval):
    """Monitorea el crecimiento de archivos en una carpeta durante un intervalo."""
    initial_sizes = get_files_sizes(folder)
    for remaining in range(interval, 0, -1):
        countdown_label.config(text=f"Time remaining: {remaining} seconds")
        countdown_label.update()
        time.sleep(1)
    final_sizes = get_files_sizes(folder)

    growth_rates = calculate_growth_rate(initial_sizes, final_sizes, interval)
    return growth_rates


def start_monitoring():
    folder = folder_entry.get()
    try:
        interval = int(interval_entry.get())
    except ValueError:
        result_text.insert(tk.END, "Invalid interval. Please enter a number.\n")
        return

    if not os.path.isdir(folder):
        result_text.insert(tk.END, "Invalid folder path\n")
        return

    result_text.insert(tk.END, f"Monitoring folder: {folder}\n")
    result_text.insert(tk.END, f"Please wait for {interval} seconds...\n")
    result_text.update()

    growth_rates = monitor_folder_growth(folder, interval)

    result_text.insert(tk.END, "\nMonitoring complete. Results:\n")
    if growth_rates:
        result_text.insert(tk.END, "Files that grew and their growth rates (bytes/second):\n")
        for file_path, rate in growth_rates.items():
            result_text.insert(tk.END, f"{file_path}: {rate:.2f} bytes/second\n")
    else:
        result_text.insert(tk.END, "No files grew during the monitoring period.\n")

    countdown_label.config(text="")


# Create the main window
root = tk.Tk()
root.title("Folder Growth Monitor")

# Create and place the folder path entry
ttk.Label(root, text="Folder to monitor:").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
folder_entry = ttk.Entry(root, width=50)
folder_entry.grid(column=1, row=0, padx=10, pady=5)

# Create and place the interval entry
ttk.Label(root, text="Interval (seconds):").grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
interval_entry = ttk.Entry(root, width=20)
interval_entry.grid(column=1, row=1, padx=10, pady=5)

# Create and place the start button
start_button = ttk.Button(root, text="Start Monitoring", command=start_monitoring)
start_button.grid(column=0, row=2, columnspan=2, padx=10, pady=5)

# Create and place the countdown label
countdown_label = ttk.Label(root, text="")
countdown_label.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

# Create and place the result text box
result_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
result_text.grid(column=0, row=4, columnspan=2, padx=10, pady=5)

# Start the main event loop
root.mainloop()
