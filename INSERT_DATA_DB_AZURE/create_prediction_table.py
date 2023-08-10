from utils import delete_table, connect_to_database

conn = connect_to_database()
cursor = conn.cursor()

delete_table('prediction')


# Créer la table "prediction"
create_films_table_query = '''
CREATE TABLE prediction (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titre VARCHAR(500),
    prediction FLOAT

);
'''
cursor.execute(create_films_table_query)
conn.commit()