# File: views.py
# Author: alexander chappuis (alexc26@bu.edu), 2/10/26
# Description: contains the views for two profile views

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse





class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"



class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = 'profile'


class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = 'post'





class CreatePostView(CreateView):
    '''handle creation of a new Post.'''

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
        ''' form submission  '''

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

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"


class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"


class DeletePostView(DeleteView):
    '''delete post'''
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        post = self.get_object()
        return reverse('show_profile', kwargs={'pk': post.profile.pk})


class ShowFollowersDetailView(DetailView):
    '''show followers'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = 'profile'


class PostFeedListView(ListView):
    '''handles the post feed'''
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=pk)
        return context


class SearchView(ListView):
    '''handles search for Profiles and Posts.'''

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in self.request.GET:
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=pk)
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        query = self.request.GET.get('query', '')
        context['profile'] = Profile.objects.get(pk=pk)
        context['query'] = query
        profiles_by_username = list(Profile.objects.filter(username__icontains=query))
        profiles_by_name = list(Profile.objects.filter(display_name__icontains=query))
        profiles_by_bio = list(Profile.objects.filter(bio_text__icontains=query))
        all_profiles = []
        seen_keys = set()
        for profile in profiles_by_username + profiles_by_name + profiles_by_bio:
            if profile.pk not in seen_keys:
                all_profiles.append(profile)
                seen_keys.add(profile.pk)
        context['profiles'] = all_profiles
        return context