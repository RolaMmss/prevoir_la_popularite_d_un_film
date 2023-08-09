from fastapi import HTTPException
import string 
import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd
import ast 
import unicodedata
import re


def update_from_azure_db():
    try:
        # Load environment variables

# Load environment variables
        load_dotenv()
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_name')
        DB_Driver = os.getenv('DB_Driver')

# Établir la connexion à votre base de données
        connection_string = f'Driver={DB_Driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = """ SELECT titre,
           MAX(duree) AS durée,
           MAX(distributeur) AS distributeur,
           MAX(realisateur) AS réalisateur,
           MAX(nationalites) AS nationalités,
           MAX(langue_d_origine) AS langue_d_origine,
           MAX(type_film) AS type_film,
           MAX(genre) AS genres,
           MAX(annee_production) AS annee_production,
           STRING_AGG(acteurs, ',') AS acteurs,
           STRING_AGG(top_acteurs.acteur, ',') AS acteurs_connus
           FROM movies
           INNER JOIN actors ON movies.id = actors.film_id
           INNER JOIN top_acteurs ON actors.id_acteurs_films = top_acteurs.id
           GROUP BY titre;
            """

        df_azure_data = pd.read_sql(query, conn)

# Fermer la connexion après utilisationS
        conn.close()

        columns_to_replace_with_zero = ['durée', 'annee_production']
        
        columns_to_check = ['durée', 'distributeur', 'réalisateur', 'nationalités', 'langue_d_origine',
                    'type_film', 'genres', 'annee_production', 'acteurs', 'acteurs_connus']

# Boucle à travers les colonnes spécifiées
        for column in columns_to_check:
                if column in columns_to_replace_with_zero:
                        df_azure_data[column].fillna(0, inplace=True)
                else:
                        df_azure_data[column].fillna('inconnu', inplace=True)





# Fonction pour nettoyer le nom d'un acteur
        def clean_name(name):
            name = name.lower()  # Convertir en minuscules
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')  # Supprimer les accents
            name = name.replace(" ", "")  # Supprimer les espaces
            return name

# Calculer le nombre d'acteurs connus
        def calculate_known_actors(row):
            actor = clean_name(row['acteurs_connus'][0])
            actors = [clean_name(a) for a in row['acteurs']]

            return sum(actor in a for a in actors)

        def calculate_known_realisateur(row):
            actor = clean_name(row['acteurs_connus'][0])
            realisateur = [clean_name(a) for a in row['réalisateur']]

            return int(any(actor in a for a in realisateur))

        df_azure_data['nombre_acteurs_connus'] = df_azure_data.apply(calculate_known_actors, axis=1)
        df_azure_data['realisateur_connu'] = df_azure_data.apply(calculate_known_realisateur, axis=1)


        df_azure_data['genres'] = df_azure_data['genres'].str.replace("[\[\]']", "", regex=True)
        df_azure_data['genres'] = df_azure_data['genres'].str.split('_')

        unique_genres = set(g for row in df_azure_data['genres'] for g in row)

        for genre in unique_genres:
                df_azure_data[genre] = df_azure_data['genres'].apply(lambda x: 1 if genre in x else 0)



        return df_azure_data

    except pyodbc.Error as err:
        raise HTTPException(status_code=500, detail=" Nooooooooooooo Error connecting to the Azure database")