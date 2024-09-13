import csv
import mysql.connector

# MariaDB connection configuration
config = {
    'user': 'root',
    'password': 'admin123',
    'host': 'localhost',
    'database': 'metro',
    'raise_on_warnings': True
}

# Connect to MariaDB
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Create table (adjust table name and column definitions as needed)
create_table_query = """
CREATE TABLE IF NOT EXISTS afluencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    linea VARCHAR(20),
    estacion VARCHAR(50),
    afluencia INT,
    periodo VARCHAR(20)
)
"""
cursor.execute(create_table_query)

# Read CSV and insert data
with open('afluencia.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        if row[0] != 'SD' and row[1] != 'SD':
            insert_query = """
            INSERT INTO afluencia (linea, estacion, afluencia, periodo)
            VALUES (%s, %s, %s, %s)
            """
            linea = row[0]
            estacion = row[1]
            afluencia = int(row[1].replace(',', '')) if row[1].replace(',', '').isdigit() else 0
            periodo = "Trimestre 1 2021"  # Adjust this based on your data
            cursor.execute(insert_query, (linea, estacion, afluencia, periodo))

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Data insertion completed.")