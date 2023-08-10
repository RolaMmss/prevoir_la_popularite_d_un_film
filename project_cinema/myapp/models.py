from django.db import models



class Film(models.Model):
    titre = models.CharField(max_length=500)
    distributeur = models.CharField(max_length=500)
   # date = models.DateField(default=timezone.now)
    type_film = models.CharField(max_length=100, default='Unknown')  # Add a default value here


    class Meta:
        db_table = 'dataset_model_ML'



class Acteurs_films(models.Model):
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)
    acteurs = models.CharField(max_length=500)

    class Meta:
        db_table = 'actors'



class Movies(models.Model):
    titre = models.CharField(max_length=500)
    class Meta:
        db_table = 'movies'


class Prediction(models.Model):
    film = models.ForeignKey(Movies, on_delete=models.CASCADE)
    prediction = models.FloatField()

    class Meta:
        db_table = 'prediction'
