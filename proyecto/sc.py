import requests
from bs4 import BeautifulSoup

url = 'https://metro.cdmx.gob.mx/operacion/mas-informacion/afluencia-de-estacion-por-linea'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extraer los datos de afluencia
tables = soup.find_all('table')  # Suponiendo que la tabla tiene la clase 'table'

for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # Procesa cada columna según sea necesario
        for col in cols:
            print(col.text)  # Aquí puedes extraer el texto de cada celda
