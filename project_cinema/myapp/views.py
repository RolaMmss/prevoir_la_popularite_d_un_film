from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from .models import Film, Acteurs_films, Movies, Prediction
from datetime import datetime
from django.forms import Form, DateField as FormDateField
from myapp.forms import UserCreateForm
import pandas as pd
from django.conf import settings
import os
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
import io
from django.db.models import Count
from wordcloud import WordCloud
import requests
import subprocess
from operator import itemgetter


def homepage(request):
    return render(request, 'pages_main/home.html')


class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



# def box_office(request):
#     films = Movies.objects.all()  # Récupérez tous les films de la base de données
#     predictions = []

#     # Parcourez la liste des films et effectuez les prédictions pour chaque film
#     for film in films:
#         data = {'titre': film.titre}

#         # URL de votre API FastAPI déployée sur Azure
#         api_url = 'http://20.164.88.206/predict/'  # Utilisez l'URL correcte de votre API

#         # Appel de l'API FastAPI
#         response = requests.post(api_url, json=data)

#         if response.status_code == 200:
#             prediction_value = response.json().get('box_office_prediction')
#             movies_instance = Movies.objects.get(titre=film.titre)  # Obtenez l'objet Movies correspondant
#             prediction_instance = Prediction(film=movies_instance, prediction=prediction_value)
#             prediction_instance.save()
#             predictions.append({'film': film, 'prediction': prediction_value})
#         else:
#             predictions.append({'film': film, 'prediction': 'Erreur'})

#     return render(request, 'pages_main/prediction_template.html', {'predictions': predictions})



def box_office(request):
    films = Movies.objects.all()  # Récupérez tous les films de la base de données
    predictions = []

    # Parcourez la liste des films et effectuez les prédictions pour chaque film
    for film in films:
        data = {'titre': film.titre}

        # URL de votre API FastAPI déployée sur Azure
        api_url = 'http://20.164.88.206/predict/'  # Utilisez l'URL correcte de votre API

        # Appel de l'API FastAPI
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            prediction_value = response.json().get('box_office_prediction')
            movies_instance = Movies.objects.get(titre=film.titre)  # Obtenez l'objet Movies correspondant
            
            # Vérifiez si un enregistrement avec le même film_id existe déjà dans la table Prediction
            existing_prediction = Prediction.objects.filter(film_id=movies_instance.id).first()
            
            if existing_prediction is None:
                # Ajoutez une nouvelle prédiction uniquement si elle n'existe pas déjà
                prediction_instance = Prediction(film_id=movies_instance.id, prediction=prediction_value)
                prediction_instance.save()
                
            box_office_divided = prediction_value // 2000  # Effectuer la division ici
            predictions.append({'film': film, 'prediction': prediction_value, 'box_office_divided': box_office_divided})
        else:
            predictions.append({'film': film, 'prediction': 'Erreur', 'box_office_divided': 'Erreur'})

    # Trier les prédictions par prédiction en ordre décroissant
    predictions = sorted(predictions, key=itemgetter('prediction'), reverse=True)
    # Sélectionner uniquement les 10 premières prédictions (top 10)
    top_10_predictions = predictions[:10]

    return render(request, 'pages_main/prediction_template.html', {'predictions': top_10_predictions})


def dashboard(request):
    films = Film.objects.all()
    df = pd.DataFrame(list(films.values()))
    type_film_counts = df['type_film'].value_counts()

    type_film_labels = type_film_counts.index
    type_film_values = type_film_counts.values
    plt.figure(figsize=(8, 5))
    plt.pie(type_film_values, labels=type_film_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Film Types Distribution - Pie Chart')
    pie_chart_path = 'film_types_distribution_pie_chart.png'
    plt.savefig(os.path.join(settings.MEDIA_ROOT, pie_chart_path))
    plt.close()

    # Prepare data for the WordCloud
    actor_counts = Acteurs_films.objects.values('acteurs').annotate(count=Count('acteurs')).order_by('-count')
    wordcloud_data = {actor['acteurs']: actor['count'] for actor in actor_counts}
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)

    # Plot the WordCloud and save it to a BytesIO buffer
    buffer = io.BytesIO()
    plt.figure(figsize=(8, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Actor Distribution - WordCloud')
    plt.savefig(buffer, format='png')
    plt.close()

    # Save the WordCloud image to the 'media' directory using FileSystemStorage
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save('actor_distribution.png', buffer)

    pie_chart_url = fs.url(pie_chart_path)
    wordcloud_url = fs.url(filename)

    context = {
        'pie_chart_url': pie_chart_url,
        'wordcloud_url': wordcloud_url,
    }
    return render(request, 'pages_main/dashboard.html', context)


import os
import subprocess
from django.http import JsonResponse

# def homepage(request):
#     success_message = request.GET.get('success_message')
#     error_message = request.GET.get('error_message')
#     return render(request, 'pages_main/home.html', {'success_message': success_message, 'error_message': error_message})

from django.shortcuts import redirect

import os
import subprocess
from django.urls import reverse

def scraping_view(request):
    if request.method == 'POST':
        # Récupérer le répertoire du fichier views.py (chemin relatif)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construire le chemin complet vers le répertoire du spider en utilisant le chemin relatif
        spider_dir = os.path.normpath(os.path.join(current_dir, 'SCRAP_NEW_DATA/scrap_films_prochainement/spiders'))
        # Exécuter le spider
        subprocess.run(["scrapy", "crawl", "next_movies_spider"], cwd=spider_dir)
        # Rediriger l'utilisateur vers la page d'accueil avec un message de succès
        return redirect(reverse('homepage') + '?scraping_success=true')

    return render(request, 'pages_main/home.html')

def scraping_boxoffice_view(request):
    if request.method == 'POST':
        # Récupérer le répertoire du fichier views.py (chemin relatif)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construire le chemin complet vers le répertoire du spider en utilisant le chemin relatif
        spider_dir = os.path.normpath(os.path.join(current_dir, 'SCRAP_NEW_DATA/scrap_films_prochainement/spiders'))
        # Exécuter le spider
        subprocess.run(["scrapy", "crawl", "recent_boxoffice_spider"], cwd=spider_dir)
        # Rediriger l'utilisateur vers la page d'accueil avec un message de succès
        return redirect(reverse('homepage') + '?scraping_success=true')

    return render(request, 'pages_main/home.html')
