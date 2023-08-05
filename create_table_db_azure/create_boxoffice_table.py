import csv
import pyodbc
from create_table_script import delete_table, connect_to_database

conn = connect_to_database()
cursor = conn.cursor()

delete_table('boxoffice')

# Créer la table "boxoffice"
create_boxoffice_table_query = '''
CREATE TABLE boxoffice (
    id INT IDENTITY(1,1) PRIMARY KEY,
    film_allocine_id INT,
    boxoffice INT,
    film_id INT,
    FOREIGN KEY (film_id) REFERENCES movies(id)
);
'''
cursor.execute(create_boxoffice_table_query)
conn.commit()

# Spécifier le chemin absolu du fichier CSV
csv_file_path = 'dataset_history_django_boxoffice.csv'

# Lire les données à partir du fichier CSV et les insérer dans les tables
print("Début de l'insertion des données...")
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for row in csvreader:
        try:
            film_allocine_id = int(row['film_id_allocine'])
            boxoffice = int(row['boxoffice'])
            
            # Recherche du film dans la table "movies" en utilisant film_id_allocine
            film_query = '''
            SELECT id FROM movies WHERE film_id_allocine = ?;
            '''
            cursor.execute(film_query, (film_allocine_id,))
            film_id_row = cursor.fetchone()
            
            if film_id_row:
                film_id = film_id_row[0]
                
                # Insérer la ligne dans la table "boxoffice" avec l'ID du film correspondant
                boxoffice_insert_query = '''
                INSERT INTO boxoffice (film_allocine_id, boxoffice, film_id)
                VALUES (?, ?, ?);
                '''
                cursor.execute(boxoffice_insert_query, (film_allocine_id, boxoffice, film_id))
                conn.commit()
                print(f"Box office inséré pour le film Allociné ID {film_allocine_id}")
            else:
                print(f"Film non trouvé pour Allociné ID {film_allocine_id}, box office non inséré.")
            
        except Exception as e:
            print(f'Erreur lors de l\'insertion des données dans la base de données boxoffice : {e}')

print("Insertion des données terminée.")

# Fermer la connexion
conn.close()
