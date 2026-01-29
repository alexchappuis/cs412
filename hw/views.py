from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.

def home(request):
    response_text = '''
        <html>
        <h1>Hello, World!</h1>
        The current time is {time.ctime()}.
        </html>

    '''

    return HttpResponse(response_text)


def home_page(request):
 
 
    template = 'hw/home.html'
    
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
    }
 
    return render(request, template, context)
    

def about(request):
 
 
    template = 'hw/about.html'
    
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
    }
 
    return render(request, template, context)