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
delete_table('dataset_model')
    
    
# Obtenir le chemin absolu du répertoire actuel
current_directory = os.path.dirname(os.path.abspath(__file__))
# Spécifier le nom du fichier CSV
csv_file_name = 'dataset_model.csv'

# Concaténer le chemin absolu avec le nom du fichier CSV
csv_file_path = os.path.join(current_directory, csv_file_name)


create_table_query = '''
        CREATE TABLE dataset_model (
            id INT IDENTITY(1,1) PRIMARY KEY,
            titre VARCHAR(500),
            date DATE,
            genre VARCHAR(1000),
            duree FLOAT,
            realisateur VARCHAR(500),
            distributeur VARCHAR(500),
            acteurs VARCHAR(1000),
            nationalites VARCHAR(500),
            langue_d_origine VARCHAR(500),
            type_film VARCHAR(500),
            annee_production VARCHAR(500),
            nombre_article VARCHAR(500),
            description VARCHAR(2000),
            film_id_allocine INT,
            image VARCHAR (1000),
            boxoffice INT,
        );
        '''

# Exécutez la requête pour créer la table
cursor.execute(create_table_query)
conn.commit()


# Spécifiez le nom de la table dans la base de données où vous souhaitez importer les données
table_name = 'dataset_model'

# Définissez le nom des colonnes dans le fichier CSV dans le même ordre que dans la table
columns = ['titre', 'date', 'genre', 'duree', 'realisateur','distributeur', 'acteurs', 'nationalites', 'langue_d_origine', 'type_film', 'annee_production','nombre_article', 'description', 'film_id_allocine', 'image', 'boxoffice' ]  # Remplacez par les noms de vos colonnes

print("Début de l'insertion des données...")
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        values = [row[column] for column in columns]
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
        cursor.execute(query, values)
        conn.commit()
        print(f"Ligne insérée : {row['titre']} - {row['date']}")  # Ajoutez d'autres colonnes que vous souhaitez afficher

print("Insertion des données terminée.")

# Fermez la connexion
conn.close()
