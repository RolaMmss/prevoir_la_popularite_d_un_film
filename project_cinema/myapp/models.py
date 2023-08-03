from django.db import models
from django.utils import timezone




class Film(models.Model):
    titre = models.CharField(max_length=500)
    distributeur = models.CharField(max_length=500)
    date = models.DateField(default=timezone.now)


    
  

    class Meta:
        db_table = 'films'