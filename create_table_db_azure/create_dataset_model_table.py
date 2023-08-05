from create_table_script import create_table_and_insert_data

# Spécifier les détails spécifiques à la table
table_name = 'dataset_model'
csv_file_name = 'dataset_model.csv'
columns = ['titre', 'date', 'genre', 'duree', 'realisateur', 'distributeur', 'acteurs', 'nationalites', 'langue_d_origine', 'type_film', 'annee_production', 'nombre_article', 'description', 'film_id_allocine', 'image', 'boxoffice']

# Spécifier la requête de création de la table
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
        boxoffice INT
    );
'''

# Spécifier le chemin absolu du fichier CSV
csv_file_path = csv_file_name


# Appeler la fonction pour créer la table et insérer les données
create_table_and_insert_data(table_name, columns, create_table_query, csv_file_path)
