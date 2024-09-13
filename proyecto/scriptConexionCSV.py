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
with open('afluencia.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Iterar sobre las tablas de la página
    for table in tables:
        rows = table.find_all('tr')
        
        # Contar el número de columnas más grande en la tabla
        max_columns = max([len(row.find_all('td')) for row in rows])

        # Iterar sobre las filas y columnas de cada tabla
        for row in rows:
            cols = row.find_all('td')
            # Extraer el contenido de cada celda y eliminar espacios innecesarios
            row_data = [col.get_text(strip=True) for col in cols]

            # Asegurarse de que cada fila tenga el mismo número de columnas que la fila más larga
            while len(row_data) < max_columns:
                row_data.append("SD")  # Rellenar con "SD" si faltan columnas
            
            # Reemplazar celdas vacías o con comas vacías por "SD"
            row_data = [cell if cell else "SD" for cell in row_data]
            
            # Si la fila contiene una nota (marcada con asterisco), no la escribimos en el archivo CSV
            if not any(cell.startswith("*") for cell in row_data):
                # Omitir cualquier fila que contenga "TOTAL" o "GRAN TOTAL" en cualquier columna
                if not any("TOTAL" in cell or "GRAN TOTAL" in cell for cell in row_data):
                    writer.writerow(row_data)

print("Datos guardados en afluencia.csv")
