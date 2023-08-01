import csv
import pyodbc
from dotenv import load_dotenv
import os




load_dotenv()
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
database = os.getenv('DB_name')
DB_Driver = os.getenv('DB_Driver')



# Établissez la connexion à votre base de données
connection_string = f'Driver={DB_Driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
conn = pyodbc.connect(connection_string)

cursor = conn.cursor()

def delete_table(table_name):
        drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
        cursor.execute(drop_table_query)
        conn.commit()

        # Delete les table s'il existent
delete_table('films_box_off')
    
    
# Obtenir le chemin absolu du répertoire actuel
current_directory = os.path.dirname(os.path.abspath(__file__))
# Spécifier le nom du fichier CSV
csv_file_name = 'movies_tous.csv'

# Concaténer le chemin absolu avec le nom du fichier CSV
csv_file_path = os.path.join(current_directory, csv_file_name)


create_table_query = '''
        CREATE TABLE films_box_off (
            id INT IDENTITY(1,1) PRIMARY KEY,
            titre VARCHAR(500),
            date VARCHAR(500),
            durée VARCHAR(500),
            réalisateur VARCHAR(500),
            distributeur VARCHAR(500),
            titre_original VARCHAR(500),
            nationalités VARCHAR(500),
            langue_d_origine VARCHAR(500),
            type_film VARCHAR(500),
            annee_production VARCHAR(500),
            budget VARCHAR(500),
            note_presse VARCHAR(500),
            note_spectateurs VARCHAR(500),
            nombre_article VARCHAR(500),
            recompenses VARCHAR(500),
            description VARCHAR(2000)
        );
        '''

# Exécutez la requête pour créer la table
cursor.execute(create_table_query)
conn.commit()


# Spécifiez le nom de la table dans la base de données où vous souhaitez importer les données
table_name = 'films_box_off'

# Définissez le nom des colonnes dans le fichier CSV dans le même ordre que dans la table
columns = ['titre', 'date', 'durée', 'réalisateur','distributeur', 'titre_original', 'nationalités', 'langue_d_origine', 'type_film', 'annee_production','budget', 'note_presse','note_spectateurs','nombre_article','recompenses', 'description' ]  # Remplacez par les noms de vos colonnes

# Ouvrez le fichier CSV et insérez les données dans la base de données
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        values = [row[column] for column in columns]
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
        cursor.execute(query, values)
        conn.commit()

# Fermez la connexion
conn.close()
