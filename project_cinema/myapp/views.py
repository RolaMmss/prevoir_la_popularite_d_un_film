from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from .models import Film, Acteurs_films
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
import urllib.parse


from django.db.models import Count
from wordcloud import WordCloud


def dashboard(request):
    return render(request, 'pages_main/dashboard.html')


def homepage(request):
    return render(request, 'pages_main/home.html')

class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



def box_office(request):
    # Fetch distinct dates from the films table
    distinct_dates = Film.objects.order_by('date').values_list('date', flat=True).distinct()

    # If the form is submitted, get the selected date from the request
    selected_date_str = request.GET.get('date_filter')

    # Initialize the films variable
    films = None

    # If a date is selected, convert it to the correct format and filter films based on the selected date
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%d/%m/%Y').date()
        films = Film.objects.filter(date=selected_date)
    return render(request, 'pages_main/Box_off_forecast.html', {'films': films, 'distinct_dates': distinct_dates, 'selected_date': selected_date_str})



def dashboard(request):
    # Query the database to get the data
    films = Film.objects.all()

    # Create a Pandas DataFrame from the queryset
    df = pd.DataFrame(list(films.values()))

    # Group by 'type_film' and count occurrences
    type_film_counts = df['type_film'].value_counts()

    # Prepare data for the bar plot
    x = type_film_counts.index
    y = type_film_counts.values

    # Create the bar plot using Matplotlib
    plt.figure(figsize=(8, 5))
    plt.bar(x, y)
    plt.xlabel('Type of Film')
    plt.ylabel('Count')
    plt.title('Film Types Distribution')
    plt.xticks(rotation=45)

    # Save the bar plot to a file (optional)
    plot_path = 'film_types_distribution.png'
    plt.savefig(os.path.join(settings.MEDIA_ROOT, plot_path))
    plt.close()

    # Prepare data for the Pie Chart
    type_film_labels = type_film_counts.index
    type_film_values = type_film_counts.values

    # Create the Pie Chart using Matplotlib
    plt.figure(figsize=(8, 5))
    plt.pie(type_film_values, labels=type_film_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Film Types Distribution - Pie Chart')

    # Save the Pie Chart to a file (optional)
    pie_chart_path = 'film_types_distribution_pie_chart.png'
    plt.savefig(os.path.join(settings.MEDIA_ROOT, pie_chart_path))
    plt.close()

    # Prepare data for the WordCloud
    actor_counts = Acteurs_films.objects.values('acteurs').annotate(count=Count('acteurs')).order_by('-count')
    wordcloud_data = {actor['acteurs']: actor['count'] for actor in actor_counts}

    # Create a WordCloud object
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

    # Get the URLs of the saved images
    bar_plot_url = fs.url(plot_path)
    pie_chart_url = fs.url(pie_chart_path)
    wordcloud_url = fs.url(filename)

    # Pass the image URLs to the template for rendering
    context = {
        'bar_plot_url': bar_plot_url,
        'pie_chart_url': pie_chart_url,
        'wordcloud_url': wordcloud_url,
    }
    return render(request, 'pages_main/dashboard.html', context)