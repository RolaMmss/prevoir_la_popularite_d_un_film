FROM python:3.9

WORKDIR /app

ENV PYTHONUNBUFFERED 1


COPY requirements.txt .

# Exécute les commandes pour mettre à jour et installer unixodbc-dev
RUN apt-get update && apt-get install -y unixodbc-dev


RUN pip install django-crispy-forms  django-widget-tweaks pyodbc


RUN apt-get update && \
      apt-get -y install sudo

# Copy dependecies and install them as root
COPY install_dependencies.sh install_dependencies.sh
RUN sh install_dependencies.sh

# Copy drivers and install them as root
COPY Driver_ODBC_Azure.sh Driver_ODBC_Azure.sh
RUN sh Driver_ODBC_Azure.sh

# Exposer le port sur lequel FastAPI écoute
EXPOSE 80

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]