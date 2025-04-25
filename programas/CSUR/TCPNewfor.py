import ctypes
from ctypes import wintypes
import psutil
import socket
import time

MIB_TCP_STATE_DELETE_TCB = 12

class MIB_TCPROW(ctypes.Structure):
    _fields_ = [
        ("dwState", wintypes.DWORD),
        ("dwLocalAddr", wintypes.DWORD),
        ("dwLocalPort", wintypes.DWORD),
        ("dwRemoteAddr", wintypes.DWORD),
        ("dwRemotePort", wintypes.DWORD),
    ]

SetTcpEntry = ctypes.windll.iphlpapi.SetTcpEntry

def ip2int(ip):
    return int.from_bytes(socket.inet_aton(ip), byteorder='little')

def port2int(port):
    return ctypes.htons(port)

def close_tcp_connection(local_ip, local_port, remote_ip, remote_port):
    row = MIB_TCPROW()
    row.dwState = MIB_TCP_STATE_DELETE_TCB
    row.dwLocalAddr = ip2int(local_ip)
    row.dwLocalPort = port2int(local_port)
    row.dwRemoteAddr = ip2int(remote_ip)
    row.dwRemotePort = port2int(remote_port)

    result = SetTcpEntry(ctypes.byref(row))

    if result == 0:
        print(f"[✓] Conexión {local_ip}:{local_port} -> {remote_ip}:{remote_port} cerrada.")
    else:
        print(f"[!] Error al cerrar conexión {remote_ip}:{remote_port} — Código: {result}")

# === CONFIGURACIÓN ===
local_ip = "10.236.174.77"
local_port = 2107
inactivity_threshold = 60  # segundos

# === MONITOREO DE CONEXIONES ===
while True:
    connections = [
        c for c in psutil.net_connections(kind='tcp')
        if c.laddr.ip == local_ip and c.laddr.port == local_port and c.status == 'ESTABLISHED'
    ]

    if not connections:
        print("No hay conexiones activas actualmente.")
        time.sleep(60)
        continue

    for conn in connections:
        pid = conn.pid
        if not pid:
            continue

        try:
            proc = psutil.Process(pid)
            net_before = proc.io_counters().other
            time.sleep(inactivity_threshold)
            net_after = proc.io_counters().other
        except (psutil.NoSuchProcess, AttributeError):
            continue

        if net_after == net_before:
            print(f"[!] Conexión inactiva por {inactivity_threshold}s. Cerrando...")
            close_tcp_connection(local_ip, local_port, conn.raddr.ip, conn.raddr.port)
        else:
            print(f"[✓] Conexión activa: {conn.raddr.ip}:{conn.raddr.port}")

    time.sleep(30)  # Espera antes de volver a escanear
