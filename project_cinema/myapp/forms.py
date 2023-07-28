from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()         # la méthode utilitaire  get_user_model, qui vous permet d’obtenir le modèle  User sans l’importer directement
        # fields = ('username', 'email', 'first_name', 'last_name')#, 'role')
        fields = ('username', 'email')#, 'role')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
    