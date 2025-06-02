import pyodbc

# Parámetros de conexión
server = '10.236.174.70'  # IP o nombre del servidor SQL remoto
database = 'CanalSur_AutomationDB'
username = 'pbsdbviewer'
password = 'pbsdbviewer'

# Cadena de conexión
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

try:
    # Conectar
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()

        # Ejecutar consulta
        cursor.execute("""
            SELECT [MediaName]
            FROM [dbo].[taListMediaUsage]
            WHERE [MediaSetId] = '8' AND [MediaTypeId] = '0'
        """)

        # Obtener resultados
        resultados = cursor.fetchall()

        for fila in resultados:
            print(fila.MediaName)

except Exception as e:
    print("Error conectando o ejecutando la consulta:", e)
