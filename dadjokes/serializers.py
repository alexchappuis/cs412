from rest_framework import serializers
from .models import *
 
class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ['id', 'joke', 'jokester', 'joke_time']
   


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'jokester', 'joke_time']
