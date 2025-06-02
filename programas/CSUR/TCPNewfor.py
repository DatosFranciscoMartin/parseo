import pyodbc

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
        SELECT [MediaName]
        FROM [dbo].[taListMediaUsage]
        WHERE [FUListActiveObjectId] = '5086'
          AND [MediaSetId] = '8'
          AND [MediaTypeId] = '0'
    """)
    for row in cursor.fetchall():
        print(row.MediaName)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Error:", e)

input("\nPresiona ENTER para salir...")