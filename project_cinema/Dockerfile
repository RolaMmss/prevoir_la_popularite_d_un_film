FROM python:3.9

WORKDIR /app

ENV PYTHONUNBUFFERED 1



RUN apt-get update && \
      apt-get -y install sudo


RUN pip install django-crispy-forms  django-widget-tweaks
COPY ./requirements.txt /app/requirements.txt


# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt



COPY . .



CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]