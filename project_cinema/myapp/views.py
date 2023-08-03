from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from .models import Film


def dashboard(request):
    return render(request, 'pages_main/dashboard.html')


def homepage(request):
    return render(request, 'pages_main/home.html')

class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



def box_office(request):
    # Récupérer les 4 premiers films depuis la base de données
    film = Film.objects.all()[:4]

    return render(request, 'pages_main/Box_off_forecast.html', {'films': film})

# def box_office(request):
#     # Récupérer tous les films depuis la base de données
#     films = Film.objects.all()

#     # Filtrer les films par date (à adapter selon vos besoins)
#     date_filter = request.GET.get('date_filter')
#     if date_filter:
#         films = films.filter(date=date_filter)

#     return render(request, 'pages_main/Box_off_forecast.html', {'films': films})

