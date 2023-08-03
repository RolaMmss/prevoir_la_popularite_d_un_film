from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from .models import Film
from datetime import datetime
from django.forms import Form, DateField as FormDateField

from myapp.forms import UserCreateForm

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from django.conf import settings


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



from pathlib import Path
import os


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
    plt.bar(x, y)
    plt.xlabel('Type of Film')
    plt.ylabel('Count')
    plt.title('Film Types Distribution')
    plt.xticks(rotation=45)

    # Save the plot to a file (optional)
    plot_path = 'media/film_types_distribution.png'
    plt.savefig(os.path.join(settings.MEDIA_ROOT, plot_path))

    # Pass the plot URL to the template for rendering
    context = {'plot_url': os.path.join(settings.MEDIA_URL, plot_path)}
    return render(request, 'pages_main/dashboard.html', context)
