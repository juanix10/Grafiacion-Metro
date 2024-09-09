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
        # Une el texto de cada celda con un espacio entre ellos
        row_text = ' '.join(col.get_text(separator=' ', strip=True) for col in cols)
        print(row_text)  # Imprime la fila completa sin saltos de línea
