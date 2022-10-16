from rest_framework import serializers
from .models import Anime, Character

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'
        
class CharacterSerializer(serializers.ModelSerializer):
    anime = serializers.CharField(source = "anime.name")
    
    class Meta:
        model = Character
        fields = ('id', 'name', 'anime', 'aliases', 'img_src')