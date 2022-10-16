from django.shortcuts import render
from rest_framework import viewsets
from .models import Anime, Character
from .serializers import AnimeSerializer, CharacterSerializer

# Create your views here.
class AnimeViewSet(viewsets.ModelViewSet):
    serializer_class = AnimeSerializer
    queryset = Anime.objects.all()
    
class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()