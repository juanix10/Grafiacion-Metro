import csv
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",
    database="metro"
)
cursor = conn.cursor()

# Variable para almacenar la línea actual
linea_actual = None
cursor.execute("CREATE DATABASE IF NOT EXISTS metro")
cursor.execute("USE metro")
cursor.execute('''CREATE TABLE IF NOT EXISTS afluencia(
                id INT AUTO_INCREMENT PRIMARY KEY,
                linea VARCHAR(50),
                estacion VARCHAR(100),
                afluencia BIGINT
               ); 
                ''');
cursor.execute("TRUNCATE TABLE afluencia");     
# Abrir el archivo CSV y procesar los datos
with open('afluencia.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    
    # Iterar sobre las filas del archivo CSV
    for row_num, row in enumerate(reader, start=1):
        print(f"Procesando fila {row_num}: {row}")  # Depuración: Mostrar cada fila
        
        # Si hay una nueva línea en la fila, actualizar la variable de línea actual
        if row[0].startswith("LÍNEA"):
            linea_actual = row[0]
            continue  # Saltar a la siguiente fila ya que esta no tiene estaciones

        # Procesar las estaciones y afluencias para la línea actual
        for i in range(0, len(row), 3):  # Salta de 3 en 3 columnas
            if i + 2 < len(row):
                estacion = row[i]
                afluencia = row[i + 1]

                # Si la estación o afluencia es "SD", se ignoran esos datos
                if estacion != "SD" and afluencia != "SD":
                    try:
                        # Convertir la afluencia en un número entero eliminando comas
                        afluencia = int(afluencia.replace(',', ''))

                        # Insertar los datos en la base de datos
                        query = "INSERT INTO afluencia (linea, estacion, afluencia) VALUES (%s, %s, %s)"
                        values = (linea_actual, estacion, afluencia)
                        cursor.execute(query, values)
                    except ValueError:
                        print(f"Error al convertir afluencia: {afluencia} en la fila {row_num}")
            else:
                print(f"Fila {row_num} tiene menos de 3 columnas: {row}")

# Confirmar la inserción de los datos
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()
