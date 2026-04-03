from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Joke, Picture
from rest_framework import generics
from .serializers import *
import random
from rest_framework.views import APIView
from .serializers import JokeSerializer, PictureSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import JokeSerializer, PictureSerializer  




class RandomListView(ListView):
    template_name = "dadjokes/index.html"
    model = Joke

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jokes = Joke.objects.all()
        pictures = Picture.objects.all()
        context['joke'] = random.choice(list(jokes)) if jokes else None
        context['picture'] = random.choice(list(pictures)) if pictures else None
        return context
    


class JokeDetailView(DetailView):
    template_name = "dadjokes/joke.html"
    model = Joke


class JokeListView(ListView):
    template_name = "dadjokes/jokes.html"
    model = Joke


class PictureListView(ListView):
    template_name = "dadjokes/pictures.html"
    model = Picture


class PictureDetailView(DetailView):
    template_name = "dadjokes/picture.html" 
    model = Picture 


class JokeListAPIView(generics.ListCreateAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListCreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomJokeAPIView(generics.RetrieveAPIView):
    serializer_class = JokeSerializer
    def get_object(self):
        jokes = list(Joke.objects.all())
        return random.choice(jokes)


class RandomPictureAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PictureSerializer
    def get_object(self):
        jokes = list(Joke.objects.all())
        return random.choice(jokes)

