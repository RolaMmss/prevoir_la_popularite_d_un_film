import pyodbc
from dotenv import load_dotenv
import os

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
