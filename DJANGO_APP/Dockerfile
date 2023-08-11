FROM python:3.9

WORKDIR /app

ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /app/requirements.txt


# Exécute les commandes pour mettre à jour et installer unixodbc-dev
RUN apt-get update && apt-get install -y unixodbc-dev


RUN pip install django-crispy-forms  django-widget-tweaks pyodbc


RUN apt-get update && \
      apt-get -y install sudo

# Copier les fichiers shell
COPY ./Driver_ODBC_Azure.sh /app/Driver_ODBC_Azure.sh
COPY ./install_dependencies.sh /app/install_dependencies.sh

# Rendez les fichiers shell exécutables et exécutez-les
RUN chmod +x /app/Driver_ODBC_Azure.sh && \
    chmod +x /app/install_dependencies.sh && \
    /bin/bash /app/Driver_ODBC_Azure.sh && \
    /bin/bash /app/install_dependencies.sh

# Exposer le port sur lequel FastAPI écoute
EXPOSE 80

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]





# docker run -p 8000:8000 --rm  -v C:\Users\impej\Documents\BRIEF\ML_recap\cine_prediction:/app impejonathan/django-cine-prediction
# docker run -p 80:80 --rm  -v C:\Users\impej\Documents\BRIEF\ML_recap\cine_prediction:/app impejonathan/django-cine-prediction