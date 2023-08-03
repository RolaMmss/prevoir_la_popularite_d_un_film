from django.db import models





class Film(models.Model):
    titre = models.CharField(max_length=500)
    distributeur = models.CharField(max_length=500)
  

    class Meta:
        db_table = 'films'