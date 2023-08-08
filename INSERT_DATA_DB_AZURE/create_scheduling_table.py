from create_table_db_azure.utils import delete_table, connect_to_database
import random

def create_scheduling_table(conn, cursor):
    delete_table('scheduling')  # Supprimer la table si elle existe déjà

    # Créer la table "scheduling"
    create_scheduling_table_query = '''
    CREATE TABLE scheduling (
        id INT IDENTITY(1,1) PRIMARY KEY,
        hall_number INT CHECK (hall_number BETWEEN 1 AND 4),
        film_id INT,
        FOREIGN KEY (film_id) REFERENCES movies(id)
    );
    '''
    cursor.execute(create_scheduling_table_query)
    conn.commit()
    print("Table 'scheduling' créée avec succès.")

def insert_random_scheduling_data(conn, cursor):
    # Obtenir les IDs des films depuis la table "movies"
    cursor.execute('SELECT id FROM movies')
    movie_ids = [row[0] for row in cursor.fetchall()]

    print("Début de l'insertion des données aléatoires dans la table 'scheduling'.")

    # Insérer des données aléatoires dans la table "scheduling"
    for movie_id in movie_ids:
        hall_number = random.randint(1, 4)  # Générer un numéro de salle aléatoire entre 1 et 4
        insert_query = 'INSERT INTO scheduling (hall_number, film_id) VALUES (?, ?);'
        cursor.execute(insert_query, (hall_number, movie_id))
        print(f"Insertion de la ligne avec film_id={movie_id} et hall_number={hall_number}.")

    conn.commit()
    print("Insertion des données terminée.")

def main():
    conn = connect_to_database()
    cursor = conn.cursor()

    create_scheduling_table(conn, cursor)
    insert_random_scheduling_data(conn, cursor)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
