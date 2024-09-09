import requests
from bs4 import BeautifulSoup

url = 'https://metro.cdmx.gob.mx/operacion/mas-informacion/afluencia-de-estacion-por-linea'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraer los datos de afluencia
tables = soup.find_all('table')  # Encuentra todas las tablas en la página

for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # Procesa cada columna
        for col in cols:
            # Elimina espacios y saltos de línea
            cleaned_text = col.get_text(separator=' ', strip=True)
            print(cleaned_text)  # Aquí puedes extraer el texto de cada celda

"""import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error

def scrape_metro_data(url):
    # Realizamos la solicitud HTTP
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    # Verificamos que la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al realizar la solicitud: {response.status_code}")
        return []

    # Parseamos el contenido HTML con Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontramos la tabla que contiene los datos de afluencia
    tabla_afluencia = soup.find('table', style='text-align: center;')
    if not tabla_afluencia:
        print("No se encontró la tabla de afluencia.")
        return []

    # Extraemos los datos de la tabla
    data = []
    for fila in tabla_afluencia.find_all('tr')[1:]:
        celdas = fila.find_all('td')
        if len(celdas) < 2:
            continue
        estacion = celdas[0].text.strip()
        afluencia_text = celdas[1].text.strip().replace(',', '')
        try:
            # Verifica si el texto de afluencia no está vacío antes de convertirlo
            if afluencia_text:
                afluencia = int(afluencia_text)  # Convertimos afluencia a entero
            else:
                afluencia = 0  # O maneja el caso como desees, por ejemplo, asigna un valor por defecto
        except ValueError:
            print(f"Valor de afluencia no válido: '{afluencia_text}'")
            continue
        data.append((estacion, afluencia))

    return data

def insert_into_mariadb(data):
    # Configura la conexión a tu base de datos MariaDB
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "123",
        "database": "metro"
    }

    try:
        # Conecta a la base de datos
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Conexión exitosa a la base de datos.")
        cursor = conn.cursor()

        # Supongamos que tienes una tabla llamada 'datos_metro'
        insert_query = "INSERT INTO datos_metro (nombre_estacion, afluencia) VALUES (%s, %s)"
        cursor.executemany(insert_query, data)

        # Guarda los cambios y cierra la conexión
        conn.commit()
    except Error as e:
        print(f"Error al conectar a la base de datos o ejecutar la consulta: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a la base de datos cerrada.")

def main():
    url = 'https://metro.cdmx.gob.mx/operacion/mas-informacion/afluencia-de-estacion-por-linea'
    metro_data = scrape_metro_data(url)
    if metro_data:
        insert_into_mariadb(metro_data)
        print("Datos insertados correctamente en la base de datos.")
    else:
        print("No se obtuvieron datos para insertar.")

if __name__ == "__main__":
    main()"""
