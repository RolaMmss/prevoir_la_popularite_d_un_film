from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from .models import Film
from datetime import datetime, timedelta


def dashboard(request):
    return render(request, 'pages_main/dashboard.html')


def homepage(request):
    return render(request, 'pages_main/home.html')

class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



# def box_office(request):
#     # Récupérer les 4 premiers films depuis la base de données
#     film = Film.objects.all()[:4]

#     return render(request, 'pages_main/Box_off_forecast.html', {'films': film})

from django.db.models import DateField
from django.db.models.functions import Cast
from django.forms import Form, DateField as FormDateField
from django import forms

class DateFilterForm(forms.Form):
    date = forms.DateField(widget=forms.Select(attrs={'onchange': 'this.form.submit();'}), required=False)


# def box_office(request):
#     # Fetch distinct dates from the films table
#     distinct_dates = Film.objects.order_by('date').values_list('date', flat=True).distinct()

#     # If the form is submitted, get the selected date from the request
#     selected_date = request.GET.get('date_filter')

#     # If a date is selected, filter films based on the selected date
#     if selected_date:
#         films = Film.objects.filter(date=selected_date)
#     else:
#         # If no date is selected, display all films
#         films = Film.objects.all()

#     return render(request, 'pages_main/Box_off_forecast.html', {'films': films, 'distinct_dates': distinct_dates})




def box_office(request):
    # Fetch distinct dates from the films table
    distinct_dates = Film.objects.order_by('date').values_list('date', flat=True).distinct()

    # If the form is submitted, get the selected date from the request
    selected_date_str = request.GET.get('date_filter')

    # Initialize the films variable
    films = None

    # If a date is selected, convert it to the correct format and filter films based on the selected date
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        films = Film.objects.filter(date=selected_date)

    return render(request, 'pages_main/Box_off_forecast.html', {'films': films, 'distinct_dates': distinct_dates, 'selected_date': selected_date_str})
