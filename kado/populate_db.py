import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kado.settings")

import django
django.setup()

from django.core.management import call_command

import json
from kado_api.models import Anime, Character

with open('characters.json', 'r+') as file:
    data = json.load(file)
    
for k, v in data.items():
    character_name = k
    anime = v['Anime']
    img_src = v['Image']
    aliases = v['Aliases'] if v['Aliases'] else None
    
    obj, created = Anime.objects.get_or_create(name=anime)
    
    Character.objects.get_or_create(name=character_name, anime=obj, img_src=img_src, aliases=aliases)