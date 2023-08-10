FROM python:3.9


# Exécute les commandes pour mettre à jour et installer unixodbc-dev
RUN apt-get update && apt-get install -y unixodbc-dev

#Ajoutez ces lignes pour installer les packages nécessaires pour OpenCV
RUN pip install fastapi pyodbc pandas joblib uvicorn

WORKDIR /app

# Copier les fichiers du répertoire local dans l'image
COPY ./API /app/API
COPY ./run.py /app/run.py
COPY ./requirements.txt /app/requirements.txt


# Copier les fichiers shell
COPY ./Driver_ODBC_Azure.sh /app/Driver_ODBC_Azure.sh
COPY ./install_dependencies.sh /app/install_dependencies.sh

# Rendez les fichiers shell exécutables et exécutez-les
RUN chmod +x /app/Driver_ODBC_Azure.sh && \
    chmod +x /app/install_dependencies.sh && \
    /bin/bash /app/Driver_ODBC_Azure.sh && \
    /bin/bash /app/install_dependencies.sh

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel FastAPI écoute
EXPOSE 80

# Commande pour lancer l'application
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80"]







