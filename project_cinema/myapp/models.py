from django.db import models





class films(models.Model):
    titre = models.CharField(max_length=500)
    date = models.CharField(max_length=500)
    # Ajoutez d'autres champs ici pour les autres colonnes de la table
