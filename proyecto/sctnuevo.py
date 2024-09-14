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

            # Reemplazar "SD" con "Afluencia" solo después de "LÍNEA"
            processed_data = []
            skip_next = False
            for cell in row_data:
                if skip_next:
                    skip_next = False
                    continue
                if "LÍNEA" in cell:
                    processed_data.append(cell)
                    processed_data.append("Afluencia")
                else:
                    processed_data.append(cell)
                # Marcar para saltar el siguiente "SD" si es necesario
                if "SD" in cell:
                    skip_next = True

            # Asegurarse de que cada fila tenga el mismo número de columnas que la fila más larga
            while len(processed_data) < max_columns:
                processed_data.append("SD")  # Rellenar con "SD" si faltan columnas

            # Reemplazar celdas vacías o con comas vacías por "SD"
            processed_data = [cell if cell else "SD" for cell in processed_data]
            
            # Si la fila contiene una nota (marcada con asterisco), no la escribimos en el archivo CSV
            if not any(cell.startswith("*") for cell in processed_data):
                # Omitir cualquier fila que contenga "TOTAL" o "GRAN TOTAL" en cualquier columna
                if not any("TOTAL" in cell or "GRAN TOTAL" in cell for cell in processed_data):
                    writer.writerow(processed_data)

print("Datos guardados en afluencia.csv")
