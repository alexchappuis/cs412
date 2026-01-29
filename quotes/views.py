from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

quotes_list = [
        "With your votes you are working for your future. It is not a holiday; it is the most serious day of work since you were born. Better to come in clothing dirty from work than with your soul filthy from having sold your right to justice.",
        "Remember this: you can have justice, or you can have two dollars. But you can t have both.",
        "We are still climbing a steep hill. We are far from the top, but we can see the top in the distance.",
]

images_list = [
    "https://www.amacad.org/sites/default/files/person/headshots/Munoz%20Marin%20LoC%20Public%20Domain.jpg",
    "https://www.fineartstorehouse.com/t/629/luis-munoz-marin-assassin-attempt-39183869.jpg.webp",
    "https://upload.wikimedia.org/wikipedia/commons/1/1a/Official_portrait_of_Puerto_Rican_Governor_Luis_Mu%C3%B1oz_Mar%C3%ADn_in_1950.jpg"
]


# Create your views here.

    

def quote(request):
 
    template = 'quotes/quote.html'
    
    context = {
        "quote": random.choice(quotes_list),
        "image": random.choice(images_list),
    }
    
 
    return render(request, template, context)
    

def show_all(request):
 
 
    template = 'quotes/show_all.html'

    context = {
        "quotes": quotes_list,
        "images": images_list,
    }
    

    return render(request, template, context)

def about(request):
    template = 'quotes/about.html'
    
    return render(request, template)