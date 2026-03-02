from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment  # Comment was missing
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm  # CreateCommentForm was missing
from django.urls import reverse


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



class CreateArticleView(CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''
 
 
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"



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