import csv
import pyodbc
from utils import delete_table, connect_to_database

conn = connect_to_database()
cursor = conn.cursor()

delete_table('actors')
delete_table('boxoffice')
delete_table('scheduling')
delete_table('movies')

# Créer la table "films"
create_films_table_query = '''
CREATE TABLE movies (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titre VARCHAR(500),
    date DATE,
    duree FLOAT,
    realisateur VARCHAR(500),
    distributeur VARCHAR(500),
    nationalites VARCHAR(500),
    langue_d_origine VARCHAR(500),
    type_film VARCHAR(500),
    annee_production INT,
    description VARCHAR(2000),
    genre VARCHAR (1000),
    film_id_allocine INT,
    image VARCHAR(1000)
);
'''
cursor.execute(create_films_table_query)
conn.commit()

# Créer la table "acteurs_films"
create_acteurs_films_table_query = '''
CREATE TABLE actors (
    id_acteurs_films INT IDENTITY(1,1) PRIMARY KEY,
    film_id INT,
    acteurs VARCHAR(500),
    FOREIGN KEY (film_id) REFERENCES movies(id)
);
'''
cursor.execute(create_acteurs_films_table_query)
conn.commit()

# Spécifier le chemin absolu du fichier CSV
csv_file_path = 'dataset_history_django_features.csv'

# Lire les données à partir du fichier CSV et les insérer dans les tables
print("Début de l'insertion des données...")
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    total_rows = sum(1 for _ in csvreader)  # Compter le nombre total de lignes dans le fichier CSV
    csvfile.seek(0)  # Remettre le curseur au début du fichier CSV
    for i, row in enumerate(csvreader, start=1):
        try:
            query = '''
            INSERT INTO movies (titre, date, duree, genre, realisateur, distributeur, nationalites, langue_d_origine, type_film, annee_production, description, film_id_allocine, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?);
            '''
            cursor.execute(query, (
                row['titre'], row['date'], row['duree'], row['genre'], row['realisateur'], row['distributeur'],
                row['nationalites'], row['langue_d_origine'], row['type_film'],
                row['annee_production'], row['description'], row['film_id_allocine'], row['image']
            ))
            conn.commit()
            film_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            
            try:
                # Insérer les acteurs dans la table "acteurs_films" en les associant avec l'ID du film
                acteur_list = row['acteurs'].split(',') if 'acteurs' in row else []
                for acteur in acteur_list:
                    acteur_query = '''
                    INSERT INTO actors (film_id, acteurs)
                    VALUES (?, ?);
                    '''
                    cursor.execute(acteur_query, (film_id, acteur.strip()))
                    conn.commit()
            except Exception as e:
                print(f'Erreur lors de l\'insertion des données dans la base de données acteurs : {e}')
            
            print(f"Ligne {i}/{total_rows} insérée : {row['titre']} - {row['date']}")
        except Exception as e:
            print(f'Erreur lors de l\'insertion des données dans la base de données films : {e}')

print("Insertion des données terminée.")

# Fermer la connexion
conn.close()
