from .utils import connect_to_database, delete_table
import csv

conn = connect_to_database()
cursor = conn.cursor()

delete_table('dataset_model')
# Spécifier les détails spécifiques à la table
table_name = 'dataset_model'
csv_file_name = 'dataset_model.csv'
columns = ['titre', 'genre', 'duree', 'realisateur', 'distributeur', 'acteurs', 'nationalites', 'langue_d_origine', 'type_film', 'annee_production', 'nombre_article', 'description', 'film_id_allocine', 'image', 'boxoffice']

# Spécifier la requête de création de la table
create_table_query = '''
    CREATE TABLE dataset_model_ML (
        id INT IDENTITY(1,1) PRIMARY KEY,
        titre VARCHAR(500),
        genre VARCHAR(1000),
        duree FLOAT,
        realisateur VARCHAR(500),
        distributeur VARCHAR(500),
        acteurs VARCHAR(1000),
        nationalites VARCHAR(500),
        langue_d_origine VARCHAR(500),
        type_film VARCHAR(500),
        annee_production INT,
        nombre_article INT,
        description VARCHAR(2000),
        film_id_allocine INT,
        image VARCHAR (1000),
        boxoffice INT
    );
'''
cursor.execute(create_table_query)
conn.commit()
# Spécifier le chemin absolu du fichier CSV
csv_file_path = csv_file_name

# Lire les données à partir du fichier CSV et les insérer dans les tables
print("Début de l'insertion des données...")
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    total_rows = sum(1 for _ in csvreader)  # Compter le nombre total de lignes dans le fichier CSV
    csvfile.seek(0)  # Remettre le curseur au début du fichier CSV
    for i, row in enumerate(csvreader, start=1):
        try:
            query = '''
            INSERT INTO dataset_model_ML (titre, duree, genre, realisateur, distributeur, nationalites, langue_d_origine, type_film, annee_production, nombre_article, description, film_id_allocine, image, boxoffice)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''
            cursor.execute(query, (
                row['titre'], row['duree'], row['genre'], row['realisateur'], row['distributeur'],
                row['nationalites'], row['langue_d_origine'], row['type_film'],
                row['annee_production'], row['nombre_article'], row['description'], row['film_id_allocine'], row['image'], row['boxoffice']
            ))
            conn.commit()
            print(f"Ligne {i}/{total_rows} insérée : {row['titre']} - {row['date']}")  # Ajoutez d'autres colonnes que vous souhaitez afficher
    
        except Exception as e:
            print(f'Erreur lors de l\'insertion des données dans la base de données films : {e}')

# # Appeler la fonction pour créer la table et insérer les données
# create_table_and_insert_data(table_name, columns, create_table_query, csv_file_path)
