import requests
from bs4 import BeautifulSoup
import mysql.connector

def scrape_metro_data(url):
    # Realizamos la solicitud HTTP
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    # Parseamos el contenido HTML con Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontramos la tabla que contiene los datos de afluencia
    tabla_afluencia = soup.find('table', style='text-align: center;')

    # Extraemos los datos de la tabla
    data = []
    for fila in tabla_afluencia.find_all('tr')[1:]:
        celdas = fila.find_all('td')
        estacion = celdas[0].text.strip()
        afluencia = int(celdas[1].text.strip().replace(',', ''))  # Convertimos afluencia a entero
        data.append((estacion, afluencia))

    return data

def insert_into_mariadb(data):
    # Configura la conexión a tu base de datos MariaDB
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "admin123",
        "database": "metro"
    }

    # Conecta a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Supongamos que tienes una tabla llamada 'datos_metro'
    insert_query = "INSERT INTO datos_metro (nombre_estacion, afluencia) VALUES (%s, %s)"
    cursor.executemany(insert_query, data)

    # Guarda los cambios y cierra la conexión
    conn.commit()
    conn.close()

def main():
    url = 'https://metro.cdmx.gob.mx/operacion/mas-informacion/afluencia-de-estacion-por-linea'
    metro_data = scrape_metro_data(url)
    insert_into_mariadb(metro_data)
    print("Datos insertados correctamente en la base de datos.")

if __name__ == "__main__":
    main()
