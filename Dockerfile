FROM python:3.9

#Ajoutez ces lignes pour installer les packages nécessaires pour OpenCV
RUN pip install fastapi pyodbc pandas joblib uvicorn

WORKDIR /app

# Copier les fichiers du répertoire local dans l'image
COPY ./API /app/API
COPY ./run.py /app/run.py
COPY ./requirements.txt /app/requirements.txt



# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel FastAPI écoute
EXPOSE 80

# Commande pour lancer l'application
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80"]