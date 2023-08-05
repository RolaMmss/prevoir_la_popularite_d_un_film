import pyodbc
from dotenv import load_dotenv
import os
import csv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les valeurs des variables d'environnement
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
database = os.getenv('DB_name')
DB_Driver = os.getenv('DB_Driver')

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    connection_string = f'Driver={DB_Driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    return conn

# Fonction pour supprimer une table
def delete_table(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
    cursor.execute(drop_table_query)
    conn.commit()
    conn.close()

# Fonction pour créer une table et insérer des données à partir d'un fichier CSV
def create_table_and_insert_data(table_name, columns, create_table_query, csv_file_path):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Supprimer la table s'il elle existe déjà
    delete_table(table_name)

    # Créer la table
    cursor.execute(create_table_query)
    conn.commit()
    
    print("Début de l'insertion des données...")
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        total_rows = sum(1 for _ in csvreader)  # Compter le nombre total de lignes dans le fichier CSV
        csvfile.seek(0)  # Remettre le curseur au début du fichier CSV

        for i, row in enumerate(csvreader, start=1):
            values = [row[column] for column in columns]
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            cursor.execute(query, values)
            conn.commit()
            print(f"Ligne {i}/{total_rows} insérée : {row['titre']} - {row['date']}")  # Ajoutez d'autres colonnes que vous souhaitez afficher

    print("Insertion des données terminée.")