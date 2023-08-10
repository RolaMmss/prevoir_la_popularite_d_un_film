from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from .models import Film, Acteurs_films, Movies
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


def homepage(request):
    return render(request, 'pages_main/home.html')

class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



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
            prediction = response.json().get('box_office_prediction')  # Utilisez la clé correcte du JSON
            predictions.append({'film': film, 'prediction': prediction})
        else:
            # Gérez les erreurs si l'appel à l'API échoue
            predictions.append({'film': film, 'prediction': 'Erreur'})

    return render(request, 'pages_main/prediction_template.html', {'predictions': predictions})


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

def start_scraping(request):
    script_dir = os.path.dirname(__file__)  # Chemin du répertoire de la vue
    scrapy_script_path = os.path.join(script_dir, '..', 'SCRAP_NEW_DATA', 'scrap_films_prochainement', 'spiders', 'next_movies_spider.py')
    
    try:
        subprocess.run(['python', scrapy_script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response_data = {'status': 'success', 'message': "Le scraping s'est terminé avec succès."}
    except subprocess.CalledProcessError as e:
        response_data = {'status': 'error', 'message': f"Erreur lors de l'exécution du scraping : {e.stderr.decode()}"}
    
    return JsonResponse(response_data)


