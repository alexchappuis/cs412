from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment  # Comment was missing
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm  # CreateCommentForm was missing
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

class MyLoginRequiredMixin(LoginRequiredMixin):
    
    def get_login_url(self) -> str:
        return reverse('login') 
    def get_logged_in_profile()


# Create your views here.

class ShowAllView(ListView):

    model = Article

    template_name = 'blog/show_all.html'

    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
 
        return super().dispatch(request, *args, **kwargs)





class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' 
    context_object_name = 'article'



class CreateArticleView(LoginRequiredMixin, CreateView):
    '''View to create a new Article instance.'''
 
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
 
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
        
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
 
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
 
        # attach user to form instance (Article object):
        form.instance.user = user
 
        return super().form_valid(form)



class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
 
 
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
 
 
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
 
 
        # calling the superclass method
        context = super().get_context_data()
 
 
        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
 
 
        # add this article into the context dictionary:
        context['article'] = article
        return context
 
 
 
 def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
 
 
		# delegate work to the superclass version of this method
        return super().form_valid(form)
        
            
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
 
 
        # create and return a URL:
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})



class UpdateArticleView(UpdateView):

    form_class = UpdateArticleForm 
    template_name = "blog/update_article_form.html"


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "blog/delete_comment_form.html"


    def get_success_url(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)

        article = comment.article


        return reverse('article', kwargs = {'pk':article.pk})


class RegistrationView(CreateView):
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''
 
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')



### REST API VIEW ###

from rest_framework import generics
from .serializers import *

class ArticleListAPIView(generic.ListAPIView):
    queryset = Articles.objects.all()
    