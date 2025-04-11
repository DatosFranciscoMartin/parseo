import pyodbc

# Configuración de la conexión
server = '10.236.174.71'  # Dirección IP o nombre del servidor
database = 'CanalSur_AutomationDB'  # Nombre de la base de datos
username = 'sa'  # Nombre de usuario
password = ''  # Contraseña

# Conectar a la base de datos utilizando el ODBC Driver 17
try:
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                f'SERVER={server};'
                                f'DATABASE={database};'
                                f'UID={username};'
                                f'PWD={password}')

    print("Conexión exitosa.")

    # Crear un cursor
    cursor = connection.cursor()

    # Ejecutar una consulta SQL
    query = """SELECT [MediaName] 
               FROM [CanalSur_AutomationDB].[dbo].[taListMediaUsage] 
               WHERE [MediaTypeId] = '2' 
                 AND [BucketId] = '2'"""  # Consulta SQL

    cursor.execute(query)

    # Obtener los resultados
    rows = cursor.fetchall()

    # Imprimir los resultados
    for row in rows:
        print(row)

except pyodbc.Error as ex:
    # Manejo de errores de conexión o consulta
    sqlstate = ex.args[0]
    print(f"Error al conectar o ejecutar la consulta: {sqlstate}")

finally:
    # Asegurarse de cerrar la conexión y el cursor
    try:
        cursor.close()
        connection.close()
    except NameError:
        # Si la conexión o el cursor no se crearon correctamente, no se hace nada
        pass
    print("Conexión cerrada.")

