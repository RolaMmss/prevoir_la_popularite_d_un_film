<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignupForm,LoginForm
=======
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
from django.conf import settings
import os

>>>>>>> 5c56ef9437575d9a6390df50010d7c400244dae7

def dashboard(request):
    return render(request, 'pages_main/dashboard.html')


def homepage(request):
    return render(request, 'myapp/homepage.html')

<<<<<<< HEAD
#########################################################
def signup(request):
    """Create a signup page view for the app.

    Args:
        request (HttpRequest): The HTTP request.
    
    Returns:
        HttpResponse: The HTTP response with the rendered signup page.    """
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('login')
    return render(request, 'myapp/signup.html', context={'form': form})
#####################################################################
def login_user(request):
    """The function login_page takes a request object and renders the login.html template with a LoginForm instance and a message. If the request method is POST, the form is validated and the user is authenticated using the provided username and password. If the authentication is successful, the user is logged in and redirected to the home page. Otherwise, an error message is displayed.
        The coach is staff and may sign in with:
            Username: Dr.Django
            Password: passworddjango
    Parameters:
        request: the HTTP request object sent by the client.

    Returns: 
        HttpResponse object that represents the rendered response of the login.html template.
    """
    form = LoginForm()
    message= ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('homepage')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'myapp/login.html', context={'form': form,'message':message})
#########################################################################""
def logout_user(request):
    """Log out the currently authenticated user and redirect them to the login page.

    Args:
        request: The HTTP request object.
    Returns:
        A redirect response to the login page.
    """
    logout(request)
    return redirect('login')
############################################################################
=======
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
>>>>>>> 5c56ef9437575d9a6390df50010d7c400244dae7
