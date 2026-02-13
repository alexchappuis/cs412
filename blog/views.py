from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
# Create your views here.

class ShowAllView(ListView):

    model = Article

    template_name = 'blog/show_all.html'

    context_object_name = "articles"





class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' 
    context_object_name = 'article'

