import requests
import csv
from bs4 import BeautifulSoup

# URL de la página con los datos de afluencia
url = 'https://metro.cdmx.gob.mx/afluencia-estacion-por-linea_2021'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar todas las tablas en la página
tables = soup.find_all('table')

# Crear un archivo CSV para guardar los datos (con codificación UTF-8)
with open('afluencia_metro_cdmx.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Iterar sobre las filas y columnas de cada tabla
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            # Decodificar el contenido de cada celda antes de escribirlo en el archivo CSV
            row_data = [col.get_text(separator=' ', strip=True).encode('utf-8').decode('utf-8') for col in cols]
            writer.writerow(row_data)

print("Datos guardados en afluencia_metro_cdmx.csv")
