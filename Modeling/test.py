import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import category_encoders as ce
from catboost import CatBoostRegressor    # For regression tasks use CatBoostRegressor, for classification use CatBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error  # For regression tasks
import pickle
import os
from dotenv import load_dotenv
import pyodbc

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
# Récupérer les valeurs des variables d'environnement
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
server = os.getenv('DB_SERVER')
database = os.getenv('DB_name')
DB_Driver = os.getenv('DB_Driver')

# Établissez la connexion à la base de données SQL Azure
connection_string = f'Driver={DB_Driver};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
conn = pyodbc.connect(connection_string)

# Créer un curseur
cursor = conn.cursor()

# Exécuter une requête SQL pour récupérer les données
query = "SELECT * FROM [dbo].[dataset_model]"
# data = pd.read_sql(query, conn)
cursor.execute(query)


# df_azure = pd.read_sql(query, conn)

# Récupérer les données résultantes sous forme de liste de tuples
df = cursor.fetchall()

# Fermer le curseur
cursor.close()

# Créer un DataFrame à partir des données
columns = [column[0] for column in cursor.columns(table='dataset_model')]
df = pd.DataFrame(df, columns=columns)

print(df)
X = df.drop(['boxoffice','titre','date','acteurs','awards','box_office_total',
        'description','nominations','note_presse','note_spectateurs', 'nombre_article','genres'], axis=1)
y = df['boxoffice']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, shuffle=True, random_state=42)