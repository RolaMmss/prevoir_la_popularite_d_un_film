from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from .models import Film, Acteurs_films, Movies, Prediction, Boxoffice
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

from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import TruncWeek
from django.utils import timezone
import datetime
from datetime import timedelta, date
from datetime import datetime


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
    selected_date = request.GET.get('date_filter')

    if selected_date:
        selected_date = datetime.strptime(selected_date, '%b. %d, %Y').date()  # Convert the selected date to a datetime object
        films = Movies.objects.filter(release_date=selected_date)
    else:
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
            # Gérez les erreurs si l'appel à l'API échoue
            predictions.append({'film': film, 'prediction': 'Erreur', 'box_office_divided': 'Erreur'})
        # Trier les prédictions par prédiction en ordre décroissant
    predictions = sorted(predictions, key=itemgetter('prediction'), reverse=True)
    # Sélectionner uniquement les 10 premières prédictions (top 10)
    top_10_predictions = predictions[:10]


    return render(request, 'pages_main/prediction_template.html', {'predictions': top_10_predictions})


def dashboard(request):
    films = Movies.objects.all()
    df = pd.DataFrame(list(films.values()))
    type_film_counts = df['genre'].value_counts()

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
    plt.figure(figsize=(8, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Actor Distribution - WordCloud')

    # Save the WordCloud image with a fixed filename
    wordcloud_filename = 'actor_distribution.png'
    plt.savefig(os.path.join(settings.MEDIA_ROOT, wordcloud_filename), format='png')
    plt.close()

    start_year = 2023  # Replace this with the desired year
    start_date = timezone.datetime(start_year, 7, 1)
    
    # Fetch movie data for the histogram
    movie_ids = Film.objects.values_list('id', flat=True)
    
    # Fetch box office data
    box_office_data = Boxoffice.objects.filter(film__id__in=movie_ids, film__date__gte=start_date)
    prediction_data = Prediction.objects.filter(film__id__in=movie_ids, film__date__gte=start_date)
    
    # Group and calculate the sum of box office and prediction per week
    box_office_sum_by_week = box_office_data.annotate(week=TruncWeek('film__date')).values('week').annotate(total_box_office=Sum('boxoffice'))
    prediction_sum_by_week = prediction_data.annotate(week=TruncWeek('film__date')).values('week').annotate(total_prediction=Sum('prediction'))
    
    # Convert the querysets to pandas dataframes
    box_office_df = pd.DataFrame(list(box_office_sum_by_week))
    prediction_df = pd.DataFrame(list(prediction_sum_by_week))
    
    # Merge dataframes on the week field
    merged_df = pd.merge(box_office_df, prediction_df, on='week', how='outer')
    merged_df = merged_df.fillna(0)  # Fill NaN with zeros
    
   # Convert 'week' column from datetime.date to datetime.datetime
    merged_df['week'] = merged_df['week'].apply(lambda x: datetime.datetime.combine(x, datetime.datetime.min.time()))
    bar_width = 0.2  # Width of each bar
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(merged_df['week'] - datetime.timedelta(days=0.2), merged_df['total_box_office'], width=bar_width, label='Actual Box Office', alpha=0.7)
    plt.bar(merged_df['week'] + datetime.timedelta(days=0.2), merged_df['total_prediction'], width=bar_width, label='Predicted Box Office', alpha=0.7)
    plt.xlabel('Week')
    plt.ylabel('Box Office Sum')
    plt.title('Box Office Sum per Week')
    plt.xticks(rotation=45)
    plt.legend()

    
    
    # Save the bar chart image
    bar_chart_path = 'box_office_by_week.png'
    plt.tight_layout()
    plt.savefig(os.path.join(settings.MEDIA_ROOT, bar_chart_path))
    plt.close()


    # Save images to the 'media' directory using FileSystemStorage
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    pie_chart_url = fs.url(pie_chart_path)
    wordcloud_url = fs.url(wordcloud_filename)
    histogram_url = fs.url(bar_chart_path)
    context = {
        'pie_chart_url': pie_chart_url,
        'wordcloud_url': wordcloud_url,
        'histogram_url': histogram_url,
    }
    
    return render(request, 'pages_main/dashboard.html', context)


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


def model_overview(request):
    return render(request, 'pages_main/model_overview.html')


def home_user(request):
    # Obtenez la date d'aujourd'hui
    today = date.today()
    # # Fetch distinct dates from the films table
    # distinct_dates = Movies.objects.order_by('-date').values_list('date', flat=True).distinct()
    # Fetch distinct dates from the films table starting from today
    distinct_dates = Movies.objects.filter(date__gte=today).order_by('date').values_list('date', flat=True).distinct()
    # If the form is submitted, get the selected date from the request
    selected_date_str = request.GET.get('date')

    # Initialize the films and predictions variables
    films = None
    top_10_predictions = []

    # If a date is selected, convert it to the correct format and filter films based on the selected date
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

#Get films for the selected date
        films = Movies.objects.filter(date=selected_date)

        # Predict box office for each film and store predictions in a list
        predictions = []
        for film in films:
            data = {'titre': film.titre}
            # URL de votre API FastAPI déployée sur Azure
            api_url = 'http://20.164.88.206/predict/'  # Utilisez l'URL correcte de votre API
#Appel de l'API FastAPI
            response = requests.post(api_url, json=data)

            if response.status_code == 200:
                prediction_value = response.json().get('box_office_prediction')
                box_office_divided = prediction_value // 2000  # Effectuer la division ici
                predictions.append({'film': film, 'prediction': prediction_value, 'box_office_divided': box_office_divided})
            else:
                # Gérez les erreurs si l'appel à l'API échoue
                predictions.append({'film': film, 'prediction': 'Erreur', 'box_office_divided': 'Erreur'})

        # Trier les prédictions par prédiction en ordre décroissant
        top_10_predictions = sorted(predictions, key=lambda x: x['prediction'], reverse=True)[:10]
    return render(request, 'pages_main/home_user.html', {'films': films, 'distinct_dates': distinct_dates, 'selected_date': selected_date_str, 'predictions': top_10_predictions})