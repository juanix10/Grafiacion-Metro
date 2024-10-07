import mysql.connector
import csv
import sys
import os
from contextlib import closing

def connect_to_mariadb():
    print("Attempting to connect to the MariaDB database...")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="metro"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

def convert_csv_to_mariadb(csv_file_path, table_name):
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"The CSV file '{csv_file_path}' does not exist.")

    print(f"Starting conversion of '{csv_file_path}' to table '{table_name}'")
    with closing(connect_to_mariadb()) as connection:
        print("Database connection established")
        with closing(connection.cursor()) as cursor:
            try:
                cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
                if cursor.fetchone():
                    confirm = input(f"Table '{table_name}' already exists. Do you want to drop and recreate it? (y/n): ")
                    if confirm.lower() != 'y':
                        print("Operation cancelled.")
                        return

                drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
                cursor.execute(drop_table_query)
                print(f"Dropped existing table '{table_name}'")
                
                with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    headers = next(csv_reader)
                    print(f"CSV headers: {headers}")

                    if "afluencia" in csv_file_path.lower():
                        create_table_query = f"""
                        CREATE TABLE {table_name} (
                            linea VARCHAR(50),
                            estacion VARCHAR(100),
                            afluencia INT
                        )
                        """
                        insert_query = f"INSERT INTO {table_name} (linea, estacion, afluencia) VALUES (%s, %s, %s)"
                    else:
                        create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'{header} TEXT' for header in headers])})"
                        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['%s' for _ in headers])})"
                    
                    print(f"Executing create table query: {create_table_query}")
                    cursor.execute(create_table_query)
                    print("Table created successfully")
                    
                    # Insert data
                    row_count = 0
                    skipped_count = 0
                    insert_data = []
                    
                    for row in csv_reader:
                        print(f"Processing row: {row}")
                        if "afluencia" in csv_file_path.lower():
                            if len(row) != 3:
                                print(f"Skipping invalid row (expected 3 columns): {row}")
                                skipped_count += 1
                                continue
                            if not row[2].strip():  # Skip rows with empty 'afluencia' values
                                print(f"Skipping row with empty 'afluencia' value: {row}")
                                skipped_count += 1
                                continue
                            try:
                                linea = row[0]
                                estacion = row[1]
                                afluencia = int(row[2]) if row[2].isdigit() else 0
                                insert_data.append((linea, estacion, afluencia))
                                row_count += 1
                            except ValueError as ve:
                                print(f"Error processing row: {row}. Error: {ve}")
                        else:
                            insert_data.append(tuple(row))
                            row_count += 1

                    # Insert all data at once
                    if insert_data:
                        try:
                            print(f"Executing bulk insert query with {len(insert_data)} rows.")
                            cursor.executemany(insert_query, insert_data)
                            print("Bulk insert executed successfully.")
                        except mysql.connector.Error as dbe:
                            print(f"Database error during bulk insert: {dbe}")
                            connection.rollback()  # Rollback changes in case of error
                            return
                    
                    try:
                        print("Committing changes to the database...")
                        connection.commit()
                        print(f"CSV file '{csv_file_path}' processed. {row_count} rows inserted into '{table_name}' table.")
                    except mysql.connector.Error as commit_error:
                        print(f"Error committing changes: {commit_error}")
                        connection.rollback()
                        print("Changes rolled back due to commit error.")
                        raise
            except Exception as e:
                print(f"Error converting CSV to MariaDB: {e}")
                connection.rollback()
                raise

def main():
    csv_file_path = 'afluencia.csv'
    table_name = 'afluencia_table'
    
    if not os.path.isfile(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' does not exist.")
        sys.exit(1)
    
    try:
        convert_csv_to_mariadb(csv_file_path, table_name)
        print(f"Successfully converted CSV file '{csv_file_path}' to MariaDB table '{table_name}'.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except csv.Error as e:
        print(f"CSV file error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()