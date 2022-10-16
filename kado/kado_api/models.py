from django.db import models

# Create your models here.
class Anime(models.Model):
    name = models.CharField(max_length=100)
    
class Character(models.Model):
    name = models.CharField(max_length=100)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    img_src = models.CharField(max_length=100)
    aliases = models.CharField(max_length=200, null=True)