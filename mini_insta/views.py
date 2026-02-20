# File: views.py
# Author: alexander chappuis (alexc26@bu.edu), 2/10/26
# Description: contains the views for two profile views

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm
from django.urls import reverse





class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"



class ProfileDetailView(DetailView):
    '''Show the details for one Profile.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = 'profile'


class PostDetailView(DetailView):
    '''Show the details for one Post.'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = 'post'





class CreatePostView(CreateView):
    '''A view to handle creation of a new Post.'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        '''return context variables.'''

        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''handles form submission  '''

        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        form.instance.profile = profile 

        saved = super().form_valid(form)

        image_url = self.request.POST.get('image_url', '')
        if image_url: 
            Photo.objects.create(post=self.object, image_url=image_url)

        return saved

    def get_success_url(self):
        '''after submitting the post go to the submission'''
        return reverse('show_post', kwargs={'pk': self.object.pk})